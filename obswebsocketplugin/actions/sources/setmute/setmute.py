from libwsctrl.protocols.obs_ws4 import obs_websocket_protocol as requests
from libwsctrl.protocols.obs_ws4 import obs_websocket_events as events
from libwsctrl.structs.callback import Callback

from obswebsocketplugin.common.connection_manager import connection_manager
from obswebsocketplugin.common.uitools import ensureAccountComboBox
from virtualstudio.common.account_manager import account_manager

ACCOUNT_COMBO = "account_combo"
SOURCENAME_COMBO = "sourcename_combo"


STATE_ACTIVE = 0x0
STATE_MUTED = 0x1

def onAppear(action):
    account_manager.registerAccountChangeCallback(action.accountChangedCB)
    action.uuid_map = ensureAccountComboBox(action, ACCOUNT_COMBO)
    index = action.getGUIParameter(ACCOUNT_COMBO, "currentIndex")
    if index is not None:
        action.account_id = action.uuid_map[index]
        initAccount(action, action.account_id)


def initAccount(action, account_id):
    connection_manager.sendMessage(account_id, requests.getSourcesList(),
                                   Callback(action.updateSources,
                                            currentSelection=action.getGUIParameter(SOURCENAME_COMBO, "currentText")))

    connection_manager.addEventListener(account_id, events.EVENT_SOURCEMUTESTATECHANGED, action.muteStateChangedCB)
    source = action.getGUIParameter(SOURCENAME_COMBO, "currentText")
    if source is not None:
        connection_manager.sendMessage(account_id, requests.getMute(source),
                                   Callback(action.setMuteState))


def onDisappear(action):
    account_manager.unregisterAccountChangeCallback(action.accountChangedCB)
    index = action.getGUIParameter(ACCOUNT_COMBO, "currentIndex")
    if index is not None:
        action.account_id = action.uuid_map[index]
        deinitAccount(action, action.account_id)
        action.account_id = None


def deinitAccount(action, account_id):
    connection_manager.removeEventListener(account_id, events.EVENT_SOURCEMUTESTATECHANGED, action.muteStateChangedCB)


def onParamsChanged(action, parameters: dict):
    index = action.getGUIParameter(ACCOUNT_COMBO, "currentIndex")
    if index is not None:
        action.account_id = action.uuid_map[index]
        connection_manager.sendMessage(action.account_id, requests.getSourcesList(),
                                       Callback(action.updateSources,
                                                currentSelection=action.getGUIParameter(SOURCENAME_COMBO,
                                                                                        "currentText")))
        source = action.getGUIParameter(SOURCENAME_COMBO, "currentText")
        if source is not None:
            connection_manager.sendMessage(action.account_id, requests.getMute(source),
                                       Callback(action.setMuteState))


def onActionExecute(action):
    index = action.getGUIParameter(ACCOUNT_COMBO, "currentIndex")
    if index is not None:
        account_id = action.uuid_map[index]
        connection_manager.sendMessage(account_id, requests.setMute(action.getGUIParameter(SOURCENAME_COMBO, "currentText"), not action.isMute))
