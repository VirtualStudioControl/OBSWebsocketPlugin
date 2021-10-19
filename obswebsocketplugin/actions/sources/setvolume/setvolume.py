from libwsctrl.protocols.obs_ws4 import obs_websocket_protocol as requests
from libwsctrl.protocols.obs_ws4 import obs_websocket_events as events
from libwsctrl.structs.callback import Callback

from obswebsocketplugin.common.connection_manager import connection_manager
from obswebsocketplugin.common.uitools import ensureAccountComboBox
from virtualstudio.common.account_manager import account_manager

ACCOUNT_COMBO = "account_combo"
SOURCENAME_COMBO = "sourcename_combo"
VOLUME_MODE_COMBO = "volume_mode_combo"

ADDITIONAL_CONTROLS = "additional_controls"


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

    connection_manager.addEventListener(account_id, events.EVENT_SOURCEVOLUMECHANGED, action.volumeChangedCB)
    source = action.getGUIParameter(SOURCENAME_COMBO, "currentText")
    if source is not None:
        connection_manager.sendMessage(account_id, requests.getVolume(source, False),
                                   Callback(action.setVolume))


def onDisappear(action):
    account_manager.unregisterAccountChangeCallback(action.accountChangedCB)
    index = action.getGUIParameter(ACCOUNT_COMBO, "currentIndex")
    if index is not None:
        action.account_id = action.uuid_map[index]
        deinitAccount(action, action.account_id)
        action.account_id = None


def deinitAccount(action, account_id):
    connection_manager.removeEventListener(account_id, events.EVENT_SOURCEVOLUMECHANGED, action.volumeChangedCB)


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
            connection_manager.sendMessage(action.account_id, requests.getVolume(source, False),
                                           Callback(action.setVolume))


def positionToVolume(position: int):
    return (0.01 * position)**4


def volumeToPosition(volume: float):
    return (volume**0.25)*100.0


def onActionExecute(action, volume: float):
    index = action.getGUIParameter(ACCOUNT_COMBO, "currentIndex")
    if index is not None:
        account_id = action.uuid_map[index]
        connection_manager.sendMessage(account_id,
                                       requests.setVolume(action.getGUIParameter(SOURCENAME_COMBO, "currentText"),
                                                          max(0.0, min(volume, 20.0)), False))

