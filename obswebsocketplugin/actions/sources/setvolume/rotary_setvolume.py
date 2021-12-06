from obswebsocketplugin.actions.sources.setvolume import setvolume
from obswebsocketplugin.actions.sources.setvolume.setvolume import *
from obswebsocketplugin.common.uitools import setAccountComboBox
from virtualstudio.common.structs.action.rotary_encoder_action import RotaryEncoderAction


class RotarySetVolumeAction(RotaryEncoderAction):

    #region handlers

    def onLoad(self):
        self.volumeChangedCB = Callback(self.onVolumeChanged)
        self.uuid_map = []

        self.volume = 0


    def onAppear(self):
        self.setGUIParameter(ADDITIONAL_CONTROLS, "currentIndex", 0)
        setvolume.onAppear(self)

    def onDisappear(self):
        setvolume.onDisappear(self)

    def onSettingsGUIAppear(self):
        pass

    def onSettingsGUIDisappear(self):
        pass

    def onParamsChanged(self, parameters: dict):
        setvolume.onParamsChanged(self, parameters)

    #endregion

    #region Action Management

    def accountChangedCB(self, uuid):
        if self.account_id is not None:
            setvolume.deinitAccount(self, self.account_id)
            self.uuid_map = setAccountComboBox(self, "account_combo")
            index = self.getGUIParameter(ACCOUNT_COMBO, "currentIndex")
            if index is not None and index != uuid:
                self.account_id = self.uuid_map[index]
                setvolume.initAccount(self, self.account_id)

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

        if self.getGUIParameter(SOURCENAME_COMBO, "currentText") not in sourceNames and len(sourceNames) > 0:
            self.setGUIParameter(SOURCENAME_COMBO, "currentIndex", 0, silent=True)
            self.setGUIParameter(SOURCENAME_COMBO, "currentText", sourceNames[0], silent=True)
        else:
            self.setGUIParameter(SOURCENAME_COMBO, "currentIndex", sourceNames.index(self.getGUIParameter(SOURCENAME_COMBO, "currentText")), silent=True)
        self.setGUIParameter(SOURCENAME_COMBO, "itemTexts", sourceNames)

    def setVolume(self, msg):
        if msg['status'] != 'ok':
            self.logger.error("Failed to retrieve mute state !" + str(msg))
            return

        if msg['name'] == self.getGUIParameter(SOURCENAME_COMBO, "currentText"):
            self.volume = msg['volume']
            self.setFaderValue(volumeToPosition(self.volume))

    def onVolumeChanged(self, msg):
        if msg['sourceName'] == self.getGUIParameter(SOURCENAME_COMBO, "currentText"):
            self.volume = msg['volume']
            self.setFaderValue(volumeToPosition(self.volume))
            self.logger.debug("Source {} has volume {}".format(msg['sourceName'], msg['volume']))

    #endregion


    # region Hardware Event Handlers

    def onKeyDown(self):
        pass

    def onKeyUp(self):
        pass

    def onRotate(self, value: int):
        onActionExecute(self, positionToVolume(value))

    # endregion
