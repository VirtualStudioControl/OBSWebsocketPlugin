from libwsctrl.protocols.obs_ws5 import requests
from libwsctrl.protocols.obs_ws5 import events
from libwsctrl.structs.callback import Callback

from obswebsocketplugin.common.connection_manager import connection_manager
from obswebsocketplugin.common.uitools import ensureAccountComboBox
from virtualstudio.common.account_manager import account_manager
from virtualstudio.common.logging import logengine

ACCOUNT_COMBO = "account_combo"
TRANSITIONNAME_COMBO = "transitionname_combo"

DURATION_CHECK = "duration_check"
DURATION_SPIN = "duration_spin"

STUDIOMODE_COMBO = "studiomode_combo"

STATE_INACTIVE = 0
STATE_ACTIVE = 1

logger = logengine.getLogger()

def onAppear(action):
    account_manager.registerAccountChangeCallback(action.accountChangedCB)
    action.uuid_map = ensureAccountComboBox(action, ACCOUNT_COMBO)
    index = action.getGUIParameter(ACCOUNT_COMBO, "currentIndex")
    if index is not None:
        action.account_id = action.uuid_map[index]
        initAccount(action, action.account_id)


def initAccount(action, account_id):
    connection_manager.sendMessage(account_id, requests.getSceneTransitionList(),
                                   Callback(action.updateTransitions,
                                            currentSelection=action.getGUIParameter(TRANSITIONNAME_COMBO, "currentText")))

    connection_manager.addEventListener(account_id, events.EVENT_CURRENTSCENETRANSITIONCHANGED, action.transitionChangedCB)
    transitionName = action.getGUIParameter(TRANSITIONNAME_COMBO, "currentText")
    if transitionName is not None:
        connection_manager.sendMessage(account_id, requests.getCurrentSceneTransition(),
                                   Callback(action.setCurrentTransition))


def onDisappear(action):
    account_manager.unregisterAccountChangeCallback(action.accountChangedCB)
    index = action.getGUIParameter(ACCOUNT_COMBO, "currentIndex")
    if index is not None:
        action.account_id = action.uuid_map[index]
        deinitAccount(action, action.account_id)
        action.account_id = None


def deinitAccount(action, account_id):
    connection_manager.removeEventListener(account_id, events.EVENT_CURRENTSCENETRANSITIONCHANGED, action.transitionChangedCB)


def onParamsChanged(action, parameters: dict):
    index = action.getGUIParameter(ACCOUNT_COMBO, "currentIndex")
    if index is not None:
        if 0 < index < len(action.uuid_map):
            logger.error("Index out of bounds: Index {} for List of length {} with contents {}".format(index, len(action.uuid_map), action.uuid_map))
        action.account_id = action.uuid_map[index]
        connection_manager.sendMessage(action.account_id, requests.getSceneTransitionList(),
                                       Callback(action.updateTransitions,
                                                currentSelection=action.getGUIParameter(TRANSITIONNAME_COMBO,
                                                                                        "currentText")))
        transitionName = action.getGUIParameter(TRANSITIONNAME_COMBO, "currentText")
        if transitionName is not None:
            connection_manager.sendMessage(action.account_id, requests.getCurrentSceneTransition(),
                                       Callback(action.setCurrentTransition))


def setTransition(action, account_id):
    connection_manager.sendMessage(account_id,
                                   requests.setCurrentSceneTransition(
                                       action.getGUIParameter(TRANSITIONNAME_COMBO, "currentText")))
    connection_manager.sendMessage(account_id,
                                   requests.setCurrentSceneTransitionDuration(
                                       action.getGUIParameter(DURATION_SPIN, "currentText")))

def transitionToProgram(account_id):
    connection_manager.sendMessage(account_id,
                                   requests.triggerStudioModeTransition())

def onActionExecute(action):
    index = action.getGUIParameter(ACCOUNT_COMBO, "currentIndex")
    if index is not None:
        account_id = action.uuid_map[index]

        if connection_manager.isInStudioMode(account_id):
            if action.getGUIParameter(STUDIOMODE_COMBO, "currentIndex") == 0:
                setTransition(action, account_id)
                transitionToProgram(account_id)
            elif action.getGUIParameter(STUDIOMODE_COMBO, "currentIndex") == 1:
                setTransition(action, account_id)
            else:
                transitionToProgram(account_id)
        else:
            setTransition(action, account_id)





