from libwsctrl.protocols.obs_ws5 import requests
from libwsctrl.protocols.obs_ws5.tools.messagetools import checkError, innerData
from libwsctrl.structs.callback import Callback
from obswebsocketplugin.common.connection_manager import connection_manager
from obswebsocketplugin.common.uitools import ensureAccountComboBox, setAccountComboBox
from virtualstudio.common.logging import logengine
from virtualstudio.common.structs.action.imagebutton_action import ImageButtonAction

from . import setcurrentscene
from .setcurrentscene import SCENENAME_COMBO, ACCOUNT_COMBO, STATE_PROGRAM, STATE_PREVIEW


class ImageButtonSetCurrentSceneAction(ImageButtonAction):

    #region handlers

    def onLoad(self):
        self.sceneSwitchCB = Callback(self.onSceneChanged)
        self.previewSwitchCB = Callback(self.onScenePreviewChanged)
        self.studioModeChangedCB = Callback(self.onStudioModeChanged)
        self.account_id = None
        self.uuid_map = []

    def onAppear(self):
        setcurrentscene.onAppear(self)

    def onDisappear(self):
        setcurrentscene.onDisappear(self)

    def onSettingsGUIAppear(self):
        pass

    def onSettingsGUIDisappear(self):
        pass

    def onParamsChanged(self, parameters: dict):
        setcurrentscene.onParamsChanged(self, parameters)

    #endregion

    #region Action Management

    def accountChangedCB(self, uuid):
        if self.account_id is not None:
            setcurrentscene.deinitAccount(self, self.account_id)
            self.uuid_map = setAccountComboBox(self, "account_combo")
            index = self.getGUIParameter(ACCOUNT_COMBO, "currentIndex")
            if index is not None and index != uuid:
                self.account_id = self.uuid_map[index]
                setcurrentscene.initAccount(self, self.account_id)

    def updateScenes(self, msg, currentSelection: str = ""):
        if not checkError(msg, self.logger):
            self.logger.error("Failed to retrieve scene list !" + str(msg))
            return

        sceneNames = []
        if currentSelection is not None:
            sceneNames.append(currentSelection)

        for scene in innerData(msg)['scenes']:
            if scene['sceneName'] not in sceneNames:
                sceneNames.append(scene['sceneName'])

        if self.getGUIParameter(SCENENAME_COMBO, "currentText") not in sceneNames and len(sceneNames) > 0:
            self.setGUIParameter(SCENENAME_COMBO, "currentIndex", 0, silent=True)
            self.setGUIParameter(SCENENAME_COMBO, "currentText", sceneNames[0], silent=True)
        else:
            self.setGUIParameter(SCENENAME_COMBO, "currentIndex", sceneNames.index(self.getGUIParameter(SCENENAME_COMBO, "currentText")), silent=True)
        self.setGUIParameter(SCENENAME_COMBO, "itemTexts", sceneNames)

    def setCurrentSceneState(self, msg):
        if not checkError(msg, self.logger):
            self.logger.error("Failed to retrieve scene state !" + str(msg))
            return
        if innerData(msg)['currentProgramSceneName'] == self.getGUIParameter(SCENENAME_COMBO, "currentText"):
            self.setState(self.getState() | STATE_PROGRAM)
        else:
            self.setState(self.getState() & ~STATE_PROGRAM)

    def setPreviewSceneState(self, msg):
        if not checkError(msg, self.logger):
            return
        if innerData(msg)['currentPreviewSceneName'] == self.getGUIParameter(SCENENAME_COMBO, "currentText"):
            self.setState(self.getState() | STATE_PREVIEW)
        else:
            self.setState(self.getState() & ~STATE_PREVIEW)

    def onStudioModeChanged(self, msg):
        if not innerData(msg)['studioModeEnabled']:
            self.setState(self.getState() & ~STATE_PREVIEW)
        else:
            index = self.getGUIParameter(ACCOUNT_COMBO, "currentIndex")
            if index is not None:
                account_id = self.uuid_map[index]
                connection_manager.sendMessage(account_id, requests.getCurrentPreviewScene(), Callback(self.setPreviewSceneState))

    def onSceneChanged(self, msg):
        if innerData(msg)['sceneName'] == self.getGUIParameter(SCENENAME_COMBO, "currentText"):
            self.setState(self.getState() | STATE_PROGRAM)
        else:
            self.setState(self.getState() & ~STATE_PROGRAM)

    def onScenePreviewChanged(self, msg):
        if innerData(msg)['sceneName'] == self.getGUIParameter(SCENENAME_COMBO, "currentText"):
            self.setState(self.getState() | STATE_PREVIEW)
        else:
            self.setState(self.getState() & ~STATE_PREVIEW)
    #endregion

    #region Hardware Event Handlers

    def onKeyDown(self):
        pass

    def onKeyUp(self):
        setcurrentscene.onActionExecute(self)

    #endregion