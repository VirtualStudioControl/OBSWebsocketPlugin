import asyncio
from threading import Thread, Lock
from typing import Optional

from libwsctrl.net.obs_websocket4_client import OBSWebsocketClient
from libwsctrl.protocols.obs_ws4 import obs_websocket_events as events
from libwsctrl.protocols.obs_ws4 import obs_websocket_protocol as requests
from libwsctrl.structs.callback import Callback
from virtualstudio.common.account_manager.account_info import AccountInfo

from aiohttp.client_exceptions import ClientConnectorError, ClientError

from virtualstudio.common.logging import logengine


class ConnectionHandler(Thread):
    def __init__(self, accountData: AccountInfo):
        super(ConnectionHandler, self).__init__()
        self.accountData: AccountInfo = accountData
        self.client: Optional[OBSWebsocketClient] = None
        self.clientLock = Lock()

        self.sendQueue = []
        self.eventQueue = []
        self.logger = logengine.getLogger()

        self.isAuthenticated = False

        self.isInStudioMode = False

    def isConnected(self) -> bool:
        return self.client is not None and self.client.isConnected()

    def generateServerAddress(self):
        return "ws://{}:{}".format(self.accountData.server, self.accountData.port)

    def run(self) -> None:
        asyncio.run(self.connectToHost())
        self.logger.debug("Thread finished !")

    async def connectToHost(self):
        rcvLoop = None
        sendLoop = None
        self.isAuthenticated = False
        with self.clientLock:
            self.client = OBSWebsocketClient(self.generateServerAddress())
            try:

                rcvLoop = self.client.recieveLoop()
                sendLoop = self.client.sendLoop()
                await self.client.connect(password=self.accountData.password,
                                          onAuthenticated=Callback(self.onAuthenticated))

            except ClientConnectorError:
                self.logger.error("Error connecting to Host: {}".format(self.generateServerAddress()))
            except ClientError:
                self.logger.error("Client Error Connecting to Host: {}".format(self.generateServerAddress()))


        if rcvLoop is not None or sendLoop is not None:
            await asyncio.gather(rcvLoop, sendLoop, return_exceptions=True)
        await self.client.close()
        self.isAuthenticated = False
        self.logger.debug("Connection Closed !")

    def requestClose(self):
        self.client.requestClose()

    def onAuthenticated(self, msg):
        if msg['status'] == 'ok':
            with self.clientLock:
                self.client.addEventListener(events.EVENT_STUDIOMODESWITCHED, Callback(self.studioModeStatusChanged))
                self.client.sendMessageJson(requests.getStudioModeStatus(), Callback(self.setStudioModeStatus))
                for args in self.eventQueue:
                    self.client.addEventListener(*args)
                self.isAuthenticated = True
                for args in self.sendQueue:
                    self.client.sendMessageJson(*args)
        else:
            self.logger.error("Authentification Failed !")
            self.isAuthenticated = False
            self.requestClose()
        self.sendQueue.clear()
        self.eventQueue.clear()

    def setStudioModeStatus(self, msg):
        self.isInStudioMode = msg['studio-mode']

    def studioModeStatusChanged(self, msg):
        self.isInStudioMode = msg['new-state']

    def sendMessageJson(self, data, callback=None):
        if not (self.isConnected() and self.isAuthenticated):
            self.sendQueue.append((data, callback))
            return
        self._sendMsgInternal(data, callback)

    def _sendMsgInternal(self, data, callback=None):
        with self.clientLock:
            self.client.sendMessageJson(data, callback)

    def addEventListener(self, event, listener):
        if not (self.isConnected() and self.isAuthenticated):
            self.eventQueue.append((event, listener))
            return
        with self.clientLock:
            self.client.addEventListener(event, listener)

    def removeEventListener(self, event, listener):
        with self.clientLock:
            return self.client.removeEventListener(event, listener)
