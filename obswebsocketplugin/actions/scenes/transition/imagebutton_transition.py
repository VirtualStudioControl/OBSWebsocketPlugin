from libwsctrl.protocols.obs_ws4 import obs_websocket_protocol as requests
from libwsctrl.protocols.obs_ws4 import obs_websocket_events as events
from libwsctrl.structs.callback import Callback
from obswebsocketplugin.common.connection_manager import connection_manager
from obswebsocketplugin.common.uitools import ensureAccountComboBox, setAccountComboBox
from virtualstudio.common.logging import logengine
from virtualstudio.common.structs.action.imagebutton_action import ImageButtonAction

from . import transition
from .transition import *

class ImageButtonTransitionAction(ImageButtonAction):

    #region handlers

    def onLoad(self):
        self.transitionChangedCB = Callback(self.onTransitionChanged)

        self.uuid_map = []

    def onAppear(self):
        transition.onAppear(self)

    def onDisappear(self):
        transition.onDisappear(self)

    def onSettingsGUIAppear(self):
        pass

    def onSettingsGUIDisappear(self):
        pass

    def onParamsChanged(self, parameters: dict):
        transition.onParamsChanged(self, parameters)

    #endregion

    #region Action Management

    def accountChangedCB(self, uuid):
        if self.account_id is not None:
            transition.deinitAccount(self, self.account_id)
            self.uuid_map = setAccountComboBox(self, "account_combo")
            index = self.getGUIParameter(ACCOUNT_COMBO, "currentIndex")
            if index is not None and index != uuid:
                self.account_id = self.uuid_map[index]
                transition.initAccount(self, self.account_id)

    def updateTransitions(self, msg, currentSelection: str = ""):
        if msg['status'] != 'ok':
            self.logger.error("Failed to retrieve transition list !" + str(msg))
            return

        transitionNames = []
        if currentSelection is not None:
            transitionNames.append(currentSelection)

        for transition in msg['transitions']:
            if transition['name'] not in transitionNames:
                transitionNames.append(transition['name'])

        if self.getGUIParameter(TRANSITIONNAME_COMBO, "currentText") not in transitionNames and len(transitionNames) > 0:
            self.setGUIParameter(TRANSITIONNAME_COMBO, "currentIndex", 0, silent=True)
            self.setGUIParameter(TRANSITIONNAME_COMBO, "currentText", transitionNames[0], silent=True)
        else:
            self.setGUIParameter(TRANSITIONNAME_COMBO, "currentIndex", transitionNames.index(self.getGUIParameter(TRANSITIONNAME_COMBO, "currentText")), silent=True)
        self.setGUIParameter(TRANSITIONNAME_COMBO, "itemTexts", transitionNames)

    def setCurrentTransition(self, msg):
        if msg['status'] != 'ok':
            self.logger.error("Failed to set transition !" + str(msg))
            return

        if msg['name'] == self.getGUIParameter(TRANSITIONNAME_COMBO, "currentText"):
            self.setState(STATE_ACTIVE)
        else:
            self.setState(STATE_INACTIVE)

    def onTransitionChanged(self, msg):
        if msg['transition-name'] == self.getGUIParameter(TRANSITIONNAME_COMBO, "currentText"):
            self.setState(STATE_ACTIVE)
        else:
            self.setState(STATE_INACTIVE)

    #endregion

    #region Hardware Event Handlers

    def onKeyDown(self):
        pass

    def onKeyUp(self):
        transition.onActionExecute(self)

    #endregion