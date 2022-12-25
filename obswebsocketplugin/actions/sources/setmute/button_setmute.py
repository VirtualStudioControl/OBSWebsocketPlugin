from libwsctrl.protocols.obs_ws5.tools.messagetools import checkError, innerData
from libwsctrl.structs.callback import Callback
from obswebsocketplugin.actions.sources.setmute import setmute
from obswebsocketplugin.actions.sources.setmute.setmute import ACCOUNT_COMBO, SOURCENAME_COMBO, STATE_MUTED, STATE_ACTIVE
from obswebsocketplugin.common.uitools import setAccountComboBox
from virtualstudio.common.structs.action.button_action import ButtonAction


class ButtonSetMuteAction(ButtonAction):

    #region handlers

    def onLoad(self):
        self.muteStateChangedCB = Callback(self.onMuteStateChanged)
        self.uuid_map = []
        self.account_id = None
        self.isMute = False

    def onAppear(self):
        setmute.onAppear(self)

    def onDisappear(self):
        setmute.onDisappear(self)

    def onSettingsGUIAppear(self):
        pass

    def onSettingsGUIDisappear(self):
        pass

    def onParamsChanged(self, parameters: dict):
        setmute.onParamsChanged(self, parameters)

    #endregion

    #region Action Management

    def accountChangedCB(self, uuid):
        if self.account_id is not None:
            setmute.deinitAccount(self, self.account_id)
            self.uuid_map = setAccountComboBox(self, "account_combo")
            index = self.getGUIParameter(ACCOUNT_COMBO, "currentIndex")
            if index is not None and index != uuid:
                self.account_id = self.uuid_map[index]
                setmute.initAccount(self, self.account_id)

    def updateSources(self, msg, currentSelection: str = ""):
        # msg = getInputList
        if not checkError(msg, self.logger):
            self.logger.error("Failed to retrieve input list !" + str(msg))
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

    def setMuteState(self, msg):
        # msg = getInputMute
        if not checkError(msg, self.logger):
            self.logger.error("Failed to retrieve mute state !" + str(msg))
            return
        self.isMute = innerData(msg)['inputMuted']
        self.updateState()

    def onMuteStateChanged(self, msg):
        if innerData(msg)['inputName'] == self.getGUIParameter(SOURCENAME_COMBO, "currentText"):
            self.isMute = innerData(msg)['inputMuted']
            self.updateState()

    def updateState(self):
        if self.isMute:
            self.setState(STATE_MUTED)
        else:
            self.setState(STATE_ACTIVE)

    #endregion

    #region Hardware Event Handlers

    def onKeyDown(self):
        pass

    def onKeyUp(self):
        setmute.onActionExecute(self)
        self.ensureLEDState()

    #endregion