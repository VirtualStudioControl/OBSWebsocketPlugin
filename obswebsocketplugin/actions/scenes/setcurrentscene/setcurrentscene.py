from libwsctrl.protocols.obs_ws5 import requests
from libwsctrl.protocols.obs_ws5 import events
from libwsctrl.structs.callback import Callback

from obswebsocketplugin.common.connection_manager import connection_manager
from obswebsocketplugin.common.uitools import ensureAccountComboBox
from virtualstudio.common.account_manager import account_manager

ACCOUNT_COMBO = "account_combo"
SCENENAME_COMBO = "scenename_combo"
STUDIOMODE_COMBO = "studiomode_combo"


STATE_PREVIEW = 0x1
STATE_PROGRAM = 0x2

def onAppear(action):
    account_manager.registerAccountChangeCallback(action.accountChangedCB)
    action.uuid_map = ensureAccountComboBox(action, ACCOUNT_COMBO)
    index = action.getGUIParameter(ACCOUNT_COMBO, "currentIndex")
    if index is not None:
        action.account_id = action.uuid_map[index]
        initAccount(action, action.account_id)


def initAccount(action, account_id):
    connection_manager.addEventListener(account_id, events.EVENT_CURRENTPROGRAMSCENECHANGED, action.sceneSwitchCB)
    connection_manager.addEventListener(account_id, events.EVENT_CURRENTPREVIEWSCENECHANGED, action.previewSwitchCB)
    connection_manager.addEventListener(account_id, events.EVENT_STUDIOMODESTATECHANGED, action.studioModeChangedCB)

    connection_manager.sendMessage(account_id, requests.getSceneList(),
                                   Callback(action.updateScenes,
                                            currentSelection=action.getGUIParameter(SCENENAME_COMBO, "currentText")))
    connection_manager.sendMessage(account_id, requests.getCurrentProgramScene(), Callback(action.setCurrentSceneState))
    connection_manager.sendMessage(account_id, requests.getCurrentPreviewScene(), Callback(action.setPreviewSceneState))


def onDisappear(action):
    account_manager.unregisterAccountChangeCallback(action.accountChangedCB)
    index = action.getGUIParameter(ACCOUNT_COMBO, "currentIndex")
    if index is not None:
        action.account_id = action.uuid_map[index]
        deinitAccount(action, action.account_id)
        action.account_id = None


def deinitAccount(action, account_id):
    connection_manager.removeEventListener(account_id, events.EVENT_CURRENTPROGRAMSCENECHANGED, action.sceneSwitchCB)
    connection_manager.removeEventListener(account_id, events.EVENT_CURRENTPREVIEWSCENECHANGED, action.previewSwitchCB)
    connection_manager.removeEventListener(account_id, events.EVENT_STUDIOMODESTATECHANGED, action.studioModeChangedCB)


def onParamsChanged(action, parameters: dict):
    index = action.getGUIParameter(ACCOUNT_COMBO, "currentIndex")
    if index is not None:
        action.account_id = action.uuid_map[index]
        connection_manager.sendMessage(action.account_id, requests.getSceneList(),
                                   Callback(action.updateScenes, currentSelection=action.getGUIParameter(SCENENAME_COMBO, "currentText")))

def onActionExecute(action):
    index = action.getGUIParameter(ACCOUNT_COMBO, "currentIndex")
    if index is not None:
        account_id = action.uuid_map[index]
        if connection_manager.isInStudioMode(account_id):
            if action.getGUIParameter(STUDIOMODE_COMBO, "currentIndex") == 0:
                connection_manager.sendMessage(account_id,
                                               requests.setCurrentProgramScene(
                                                   action.getGUIParameter(SCENENAME_COMBO, "currentText")))
            else:
                connection_manager.sendMessage(account_id,
                                               requests.setCurrentPreviewScene(
                                                   action.getGUIParameter(SCENENAME_COMBO, "currentText")))
        else:
            connection_manager.sendMessage(account_id,
                                       requests.setCurrentProgramScene(action.getGUIParameter(SCENENAME_COMBO, "currentText")))