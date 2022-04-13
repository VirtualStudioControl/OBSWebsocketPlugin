from libwsctrl.protocols.obs_ws4 import obs_websocket_protocol as requests
from libwsctrl.protocols.obs_ws4 import obs_websocket_events as events
from libwsctrl.structs.callback import Callback

from obswebsocketplugin.common.connection_manager import connection_manager
from obswebsocketplugin.common.group_manager import group_manager
from obswebsocketplugin.common.uitools import ensureAccountComboBox
from obswebsocketplugin.common.structs.obs_scene_item import *
from virtualstudio.common.account_manager import account_manager
from virtualstudio.common.logging import logengine

ACCOUNT_COMBO = "account_combo"
SOURCENAME_COMBO = "sourcename_combo"
GROUP_COMBO = "group_combo"
CONSISTENCY_CHECK = "consistency_check"

STATE_INVISIBLE = 0x0
STATE_VISIBLE = 0x1
STATE_INCONSISTENT = 0x2

logger = logengine.getLogger()


def onLoad(action):
    group = action.getGUIParameter(GROUP_COMBO, "currentText")

    if group is not None and group != "":
        group_manager.addToGroup(group_manager.GROUP_TYPE_SOURCE_VISIBILITY, group, action)
    action.group = group


def onAppear(action):
    account_manager.registerAccountChangeCallback(action.accountChangedCB)
    action.uuid_map = ensureAccountComboBox(action, ACCOUNT_COMBO)
    index = action.getGUIParameter(ACCOUNT_COMBO, "currentIndex")


    if index is not None:
        action.account_id = action.uuid_map[index]
        initAccount(action, action.account_id)
        updateState(action)


def initAccount(action, account_id):
    connection_manager.sendMessage(account_id, requests.getSourcesList(),
                                   Callback(action.updateSources,
                                            currentSelection=action.getGUIParameter(SOURCENAME_COMBO, "currentText")))

    connection_manager.addEventListener(account_id, events.EVENT_SCENEITEMVISIBILITYCHANGED,
                                        action.sceneItemVisibilityChanged)
    source = action.getGUIParameter(SOURCENAME_COMBO, "currentText")
    if source is not None:
        pass
        #connection_manager.sendMessage(account_id, requests.getMute(source),
        #                           Callback(action.setMuteState))


def onDisappear(action):
    account_manager.unregisterAccountChangeCallback(action.accountChangedCB)
    index = action.getGUIParameter(ACCOUNT_COMBO, "currentIndex")
    if index is not None:
        action.account_id = action.uuid_map[index]
        deinitAccount(action, action.account_id)
        action.account_id = None


def deinitAccount(action, account_id):
    connection_manager.removeEventListener(account_id, events.EVENT_SCENEITEMVISIBILITYCHANGED,
                                           action.sceneItemVisibilityChanged)


def onParamsChanged(action, parameters: dict):
    index = action.getGUIParameter(ACCOUNT_COMBO, "currentIndex")
    if index is not None and index < len(action.uuid_map):
        action.account_id = action.uuid_map[index]
        connection_manager.sendMessage(action.account_id, requests.getSourcesList(),
                                       Callback(action.updateSources,
                                                currentSelection=action.getGUIParameter(SOURCENAME_COMBO,
                                                                                        "currentText")))
        source = action.getGUIParameter(SOURCENAME_COMBO, "currentText")

        group = action.getGUIParameter(GROUP_COMBO, "currentText")

        if action.group != group:
            if action.group is not None and action.group != "":
                group_manager.removeFromGroup(group_manager.GROUP_TYPE_SOURCE_VISIBILITY, action.group, action)
            if group is not None and group != "":
                group_manager.addToGroup(group_manager.GROUP_TYPE_SOURCE_VISIBILITY, action.group, action)

        action.group = group
        if source is not None:
            updateState(action)


def updateState(action, newstate=None):
    connection_manager.sendMessage(action.account_id, requests.getSceneList(), Callback(processSceneList, action=action, newstate=newstate))

def processSceneList(msg, action, newstate=None):
    if msg['status'] != 'ok':
        logger.error("Failed to retrieve scene list !" + str(msg))
        return

    enforce_consistency = action.getGUIParameter(CONSISTENCY_CHECK, "checked")
    sourceName = action.getGUIParameter(SOURCENAME_COMBO, "currentText")

    scenes = msg['scenes']

    state_checked = newstate
    state_inconsistent = False

    for scene in scenes:
        for source in scene['sources']:
            if source[SCENE_ITEM_NAME] == sourceName:
                if state_checked is None:
                    state_checked = source[SCENE_ITEM_RENDER]
                if state_checked != source[SCENE_ITEM_RENDER]:
                    state_inconsistent = True

    if enforce_consistency:
        sendStateToOBS(state_checked)
        state_inconsistent = False

    setState(action, state_checked, state_inconsistent)


def setState(action, state_checked, state_inconsistent):
    if state_inconsistent:
        action.setState(STATE_INCONSISTENT)
        return

    if state_checked:
        action.setState(STATE_VISIBLE)
    else:
        action.setState(STATE_INVISIBLE)


def sendStateToOBS(action, render=False):
    index = action.getGUIParameter(ACCOUNT_COMBO, "currentIndex")
    if index is not None:
        account_id = action.uuid_map[index]
        connection_manager.sendMessage(account_id, requests.getSceneList(), Callback(sendSourceState, action=action,
                                                                                     account_id=account_id))


def sendSourceState(action, account_id, msg, render=False):
    if msg['status'] != 'ok':
        logger.error("Failed to retrieve scene list !" + str(msg))
        return

    sourceName = action.getGUIParameter(SOURCENAME_COMBO, "currentText")

    scenes = msg['scenes']

    for scene in scenes:
        for source in scene['sources']:
            if source[SCENE_ITEM_NAME] == sourceName:
                connection_manager.sendMessage(account_id, requests.setSceneItemRender(scene_name=scene['name'],
                                                                                       source=sourceName,
                                                                                       render=render))


def onActionExecute(action):
    index = action.getGUIParameter(ACCOUNT_COMBO, "currentIndex")
    if index is not None:
        account_id = action.uuid_map[index]
        connection_manager.sendMessage(account_id, requests.getSceneList(), Callback(sendMessageRequests, action=action,
                                                                                     account_id=account_id))


def sendMessageRequests(action, account_id, msg):
    if msg['status'] != 'ok':
        logger.error("Failed to retrieve scene list !" + str(msg))
        return

    groupName = action.getGUIParameter(GROUP_COMBO, "currentText")

    if groupName is None:
        groupName = ""

    group = group_manager.getGroup(group_manager.GROUP_TYPE_SOURCE_VISIBILITY, groupName)

    sourceName = action.getGUIParameter(SOURCENAME_COMBO, "currentText")

    scenes = msg['scenes']

    action.render = not action.render

    logger.info("Visibility Group: {}".format(group))
    if group is not None and len(group) > 1:
        for element in group:
            if element != action:
                element.setInvisible()
        action.render = True

    for scene in scenes:
        for source in scene['sources']:
            if source[SCENE_ITEM_NAME] == sourceName:
                connection_manager.sendMessage(account_id, requests.setSceneItemRender(scene_name=scene['name'],
                                                                                       source=sourceName,
                                                                                       render=action.render))
