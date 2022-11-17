from typing import Dict, Any

from libwsctrl.net.obs_websocket4_client import OBSWebsocketClient
from obswebsocketplugin.common.connection_manager.connection_handler import ConnectionHandler
from virtualstudio.common.account_manager import account_manager
from virtualstudio.common.account_manager.account_info import AccountInfo
from virtualstudio.common.logging import logengine

CONNECTIONS: Dict[str, ConnectionHandler] = {}

logger = logengine.getLogger()

def initialise():
    account_manager.registerAccountChangeCallback(reconnectClient)


def createClient(account: AccountInfo):
    logger.debug("Creating new Client")
    connectionHandler = ConnectionHandler(account)
    CONNECTIONS[account.uuid] = connectionHandler
    connectionHandler.start()

def reconnectClient(uuid: str):
    logger.debug("Trying to reconnect")
    if uuid in CONNECTIONS:
        CONNECTIONS[uuid].requestClose()
        del CONNECTIONS[uuid]
        logger.debug("Connection Deleted")


def sendMessage(account_uuid, message, callback=None):
    if account_uuid not in CONNECTIONS:
        account = account_manager.getAccountByUUID(account_uuid)
        createClient(account)

    CONNECTIONS[account_uuid].sendMessageJson(message, callback)


def addEventListener(account_uuid, event, listener):
    if account_uuid not in CONNECTIONS:
        account = account_manager.getAccountByUUID(account_uuid)
        createClient(account)

    CONNECTIONS[account_uuid].addEventListener(event, listener)


def removeEventListener(account_uuid, event, listener):
    if account_uuid not in CONNECTIONS:
        account = account_manager.getAccountByUUID(account_uuid)
        createClient(account)

    CONNECTIONS[account_uuid].removeEventListener(event, listener)


def isInStudioMode(account_uuid):
    if account_uuid in CONNECTIONS:
        return CONNECTIONS[account_uuid].isInStudioMode
    return False