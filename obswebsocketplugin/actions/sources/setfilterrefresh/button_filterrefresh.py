from obswebsocketplugin.common.filter_data_manager import filter_data_manager
from virtualstudio.common.structs.action.button_action import ButtonAction


class ButtonFilterRefreshAction(ButtonAction):

    #region handlers

    def onLoad(self):
        pass

    def onAppear(self):
        pass

    def onDisappear(self):
        pass

    def onSettingsGUIAppear(self):
        pass

    def onSettingsGUIDisappear(self):
        pass

    def onParamsChanged(self, parameters: dict):
        pass

    #endregion


    #region Hardware Event Handlers

    def onKeyDown(self):
        pass

    def onKeyUp(self):
        filter_data_manager.updateFilterDataActions()
        self.ensureLEDState()
    #endregion