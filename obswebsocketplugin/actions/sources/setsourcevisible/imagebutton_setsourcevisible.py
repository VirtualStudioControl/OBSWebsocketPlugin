from libwsctrl.structs.callback import Callback
from obswebsocketplugin.actions.sources.setsourcevisible import setsourcevisible
from obswebsocketplugin.common.uitools import setAccountComboBox
from virtualstudio.common.structs.action.imagebutton_action import ImageButtonAction


class ImageButtonSetSourceVisibleAction(ImageButtonAction):

    # region handlers

    def onLoad(self):
        self.sceneItemVisibilityChanged = Callback(self.onSceneItemVisibilityChanged)
        self.uuid_map = []

        self.account_id = None
        self.render = False
        self.group = ""

        setsourcevisible.onLoad(self)

    def onAppear(self):
        setsourcevisible.onAppear(self)

    def onDisappear(self):
        setsourcevisible.onDisappear(self)

    def onSettingsGUIAppear(self):
        pass

    def onSettingsGUIDisappear(self):
        pass

    def onParamsChanged(self, parameters: dict):
        setsourcevisible.onParamsChanged(self, parameters)

    # endregion

    # region Action Management

    def accountChangedCB(self, uuid):
        if self.account_id is not None:
            setsourcevisible.deinitAccount(self, self.account_id)
            self.uuid_map = setAccountComboBox(self, "account_combo")
            index = self.getGUIParameter(setsourcevisible.ACCOUNT_COMBO, "currentIndex")
            if index is not None and index != uuid:
                self.account_id = self.uuid_map[index]
                setsourcevisible.initAccount(self, self.account_id)

    def updateSources(self, msg, currentSelection: str = ""):
        if msg['status'] != 'ok':
            self.logger.error("Failed to retrieve scene list !" + str(msg))
            return

        sourceNames = []
        if currentSelection is not None:
            sourceNames.append(currentSelection)

        for source in msg['sources']:
            if source['name'] not in sourceNames:
                sourceNames.append(source['name'])

        if self.getGUIParameter(setsourcevisible.SOURCENAME_COMBO, "currentText") not in sourceNames and len(
                sourceNames) > 0:
            self.setGUIParameter(setsourcevisible.SOURCENAME_COMBO, "currentIndex", 0, silent=True)
            self.setGUIParameter(setsourcevisible.SOURCENAME_COMBO, "currentText", sourceNames[0], silent=True)
        else:
            self.setGUIParameter(setsourcevisible.SOURCENAME_COMBO, "currentIndex",
                                 sourceNames.index(
                                     self.getGUIParameter(setsourcevisible.SOURCENAME_COMBO, "currentText")),
                                 silent=True)
        self.setGUIParameter(setsourcevisible.SOURCENAME_COMBO, "itemTexts", sourceNames)

    def onSceneItemVisibilityChanged(self, msg):
        if msg['item-name'] == self.getGUIParameter(setsourcevisible.SOURCENAME_COMBO, "currentText"):
            setsourcevisible.updateState(self, newstate = msg['item-visible'])

    def setInvisible(self):
        setsourcevisible.sendStateToOBS(self, render=False)

    # endregion

    # region Hardware Event Handlers

    def onKeyDown(self):
        pass

    def onKeyUp(self):
        setsourcevisible.onActionExecute(self)

    # endregion