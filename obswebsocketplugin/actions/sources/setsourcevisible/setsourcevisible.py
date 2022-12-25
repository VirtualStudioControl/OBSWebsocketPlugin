import asyncio
from asyncio import Semaphore
from typing import Callable

from libwsctrl.protocols.obs_ws5 import requests
from libwsctrl.protocols.obs_ws5 import events
from libwsctrl.protocols.obs_ws5.tools.messagetools import checkError, innerData
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
        source = action.getGUIParameter(SOURCENAME_COMBO, "currentText")
        if source is not None:
            connection_manager.sendMessage(action.account_id, requests.getSceneList(),
                                           Callback(iterateOverAllScenes, action=action,
                                                    callable=processSceneListByName))


def initAccount(action, account_id):
    connection_manager.sendMessage(account_id, requests.getInputList(),
                                   Callback(action.updateSources,
                                            currentSelection=action.getGUIParameter(SOURCENAME_COMBO, "currentText")))

    connection_manager.addEventListener(account_id, events.EVENT_SCENEITEMENABLESTATECHANGED,
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
    connection_manager.removeEventListener(account_id, events.EVENT_SCENEITEMENABLESTATECHANGED,
                                           action.sceneItemVisibilityChanged)


def onParamsChanged(action, parameters: dict):
    index = action.getGUIParameter(ACCOUNT_COMBO, "currentIndex")
    if index is not None and index < len(action.uuid_map):
        action.account_id = action.uuid_map[index]
        connection_manager.sendMessage(action.account_id, requests.getInputList(),
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
            connection_manager.sendMessage(action.account_id, requests.getSceneList(),
                                       Callback(iterateOverAllScenes, action=action, callable=processSceneListByName))

def updateState(action, sceneName, itemID, isEnabled):
    connection_manager.sendMessage(action.account_id, requests.getSceneList(), Callback(iterateOverAllScenes, action=action, callable=processSceneListByID,
                                                                                        itemID=itemID, isEnabled=isEnabled))

def iterateOverAllScenes(msg, action, callable: Callable, **kwargs):
    asyncio.create_task(iterateOverAllScenesAsync(msg, action, callable, **kwargs))
async def iterateOverAllScenesAsync(msg, action, callable: Callable, **kwargs):
    # msg = getSceneList()
    data = innerData(msg)
    enforce_consistency = action.getGUIParameter(CONSISTENCY_CHECK, "checked")

    state_checked = {}

    sem = Semaphore()
    for scene in data["scenes"]:
        name = scene["sceneName"]
        callback = Callback(callable, action=action, semaphore=sem, result=state_checked, sceneName=name, **kwargs)

        await sem.acquire()
        connection_manager.sendMessage(action.account_id, requests.getSceneItemList(sceneName=name), callback)

    await sem.acquire()
    sem.release()

    state_off = 0
    state_on = 0

    for sceneName in state_checked:
        if state_checked[sceneName]:
            state_on += 1
        else:
            state_off += 1

    state = state_on >= state_off
    isInconsistent = (state_off > 0 and state_on > 0)


    if enforce_consistency:
        sendStateToOBS(action, state)
        isInconsistent = False

    setState(action, state, isInconsistent)

def processSceneListByName(msg, action, result, sceneName, semaphore: Semaphore=None):
    # msg = getSceneItemList
    if not checkError(msg, logger):
        logger.error("Failed to retrieve scene list !" + str(msg))
        return

    sourceName = action.getGUIParameter(SOURCENAME_COMBO, "currentText")

    for source in innerData(msg)['sceneItems']:
        if source[SCENE_ITEM_NAME] == sourceName:
                result[sceneName] = source[SCENE_ITEM_RENDER]

    if semaphore != None:
        semaphore.release()


def processSceneListByID(msg, action, sceneName, itemID, isEnabled, result, semaphore: Semaphore=None):
    # msg = getSceneItemList
    if not checkError(msg, logger):
        logger.error("Failed to retrieve scene list !" + str(msg))
        return

    sourceName = action.getGUIParameter(SOURCENAME_COMBO, "currentText")

    for source in innerData(msg)['sceneItems']:
        if source[SCENE_ITEM_ID] == itemID and source[SCENE_ITEM_NAME] == sourceName:
            result[sceneName] = source[SCENE_ITEM_RENDER]

    if semaphore != None:
        semaphore.release()

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
                                                                                     account_id=account_id, render=render))


def sendSourceState(action, account_id, msg, render=False):
    # msg = getSceneList

    if not checkError(msg, logger):
        logger.error("Failed to retrieve scene list !" + str(msg))
        return

    scenes = innerData(msg)['scenes']

    for scene in scenes:
        connection_manager.sendMessage(account_id, requests.getSceneItemList(scene["sceneName"]),
                                       Callback(_sendSourceStateScene, action=action, account_id=account_id, sceneName=scene["sceneName"], render=render))

def onActionExecute(action):
    index = action.getGUIParameter(ACCOUNT_COMBO, "currentIndex")
    if index is not None:
        account_id = action.uuid_map[index]
        connection_manager.sendMessage(account_id, requests.getSceneList(), Callback(sendMessageRequests, action=action,
                                                                                     account_id=account_id))


def sendMessageRequests(action, account_id, msg):
    #msg = getSceneList
    if not checkError(msg, logger):
        logger.error("Failed to retrieve scene list !" + str(msg))
        return

    groupName = action.getGUIParameter(GROUP_COMBO, "currentText")

    if groupName is None:
        groupName = ""

    group = group_manager.getGroup(group_manager.GROUP_TYPE_SOURCE_VISIBILITY, groupName)

    sourceName = action.getGUIParameter(SOURCENAME_COMBO, "currentText")

    scenes = innerData(msg)['scenes']

    action.render = not action.render

    logger.info("Visibility Group: {}".format(group))
    if group is not None and len(group) > 1:
        for element in group:
            if element != action:
                element.setInvisible()
        action.render = True

    for scene in scenes:
        connection_manager.sendMessage(account_id, requests.getSceneItemList(scene["sceneName"]),
                                       Callback(_sendSourceStateScene, action=action, account_id=account_id, sceneName=scene["sceneName"], render=action.render))

def _sendSourceStateScene(action, account_id, msg, sceneName, render=False):
    # msg = getSceneItemList
    if not checkError(msg, logger):
        logger.error("Failed to retrieve scene item list !" + str(msg))
        return

    sourceName = action.getGUIParameter(SOURCENAME_COMBO, "currentText")
    for source in innerData(msg)['sceneItems']:
        if source[SCENE_ITEM_NAME] == sourceName:
            connection_manager.sendMessage(account_id, requests.setSceneItemEnabled(sceneName=sceneName,
                                                                                    sceneItemId=source["sceneItemId"],
                                                                                    sceneItemEnabled=render))
