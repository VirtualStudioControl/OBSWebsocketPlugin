from libwsctrl.protocols.obs_ws5.tools.messagetools import checkError, innerData
from obswebsocketplugin.actions.sources.setvolume import setvolume
from obswebsocketplugin.actions.sources.setvolume.setvolume import *
from obswebsocketplugin.common.uitools import setAccountComboBox
from virtualstudio.common.structs.action.fader_action import FaderAction


class FaderSetVolumeAction(FaderAction):

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

    def updateSources(self, msg, currentSelection: str = None):
        # msg = getInputList
        if not checkError(msg, self.logger):
            self.logger.error("Failed to retrieve scene list !" + str(msg))
            return

        sourceNames = []
        if currentSelection is not None:
            sourceNames.append(currentSelection)

        for source in innerData(msg)['inputs']:
            if source['inputName'] not in sourceNames:
                sourceNames.append(source['inputName'])

        if self.getGUIParameter(SOURCENAME_COMBO, "currentText") not in sourceNames and len(sourceNames) > 0:
            self.setGUIParameter(SOURCENAME_COMBO, "currentIndex", 0, silent=True)
            self.setGUIParameter(SOURCENAME_COMBO, "currentText", sourceNames[0], silent=True)
        else:
            self.setGUIParameter(SOURCENAME_COMBO, "currentIndex", sourceNames.index(self.getGUIParameter(SOURCENAME_COMBO, "currentText")), silent=True)
        self.setGUIParameter(SOURCENAME_COMBO, "itemTexts", sourceNames)

    def setVolume(self, msg):
        # msg = getInputVolume
        if not checkError(msg, self.logger):
            self.logger.error("Failed to retrieve mute state !" + str(msg))
            return

        self.volume = innerData(msg)['inputVolumeMul']

    def onVolumeChanged(self, msg):
        if innerData(msg)['inputName'] == self.getGUIParameter(SOURCENAME_COMBO, "currentText"):
            self.volume = innerData(msg)['inputVolumeMul']
            self.setFaderValue(volumeToPosition(self.volume))
            self.logger.debug("Source {} has volume {}".format(msg['sourceName'], msg['volume']))

    #endregion

    # region Hardware Event Handlers

    def onTouchStart(self):
        pass

    def onTouchEnd(self):
        pass

    def onMove(self, value):
        onActionExecute(self, positionToVolume(value))

    # endregion
