from typing import Dict, Optional

from libwsctrl.structs.callback import Callback
from obswebsocketplugin.actions.sources.setfiltervalue import setfiltervalue
from obswebsocketplugin.actions.sources.setfiltervalue.setfiltervalue import FILTER_VALUE_COMBO
from obswebsocketplugin.common.structs.obs_filter import OBSFilter
from obswebsocketplugin.common.uitools import setAccountComboBox
from virtualstudio.common.structs.action.fader_action import FaderAction


class FaderSetFilterValue(FaderAction):

    #region handlers

    def onLoad(self):
        self.control_page = setfiltervalue.PAGE_SLIDER
        self.uuid_map = []
        self.account_id = None

        self.filters: Dict[str, OBSFilter] = {}
        self.filter: Optional[OBSFilter] = None

        self.prevuivals = {}
        self.value_type = 0

        setfiltervalue.onLoad(self)

    def onAppear(self):
        #self.setGUIParameter(setfiltervalue, "currentIndex", 0)
        setfiltervalue.onAppear(self)

    def onDisappear(self):
        setfiltervalue.onDisappear(self)

    def onSettingsGUIAppear(self):
        pass

    def onSettingsGUIDisappear(self):
        pass

    def onParamsChanged(self, parameters: dict):
        setfiltervalue.onParamsChanged(self, parameters)

    def updateFilterValues(self):
        setfiltervalue.updateFilterValues(self)

    def updateHardware(self):
        valName = self.getGUIParameter(setfiltervalue.FILTER_VALUE_COMBO, "currentText")
        val = setfiltervalue.mapValueToHardware(self, self.filter.settings[valName])

        self.setFaderValue(val)

    #endregion

    #region Action Management

    def accountChangedCB(self, uuid):
        if self.account_id is not None:
            setfiltervalue.deinitAccount(self, self.account_id)
            self.uuid_map = setAccountComboBox(self, "account_combo")
            index = self.getGUIParameter(setfiltervalue.ACCOUNT_COMBO, "currentIndex")
            if index is not None and index != uuid:
                self.account_id = self.uuid_map[index]
                setfiltervalue.initAccount(self, self.account_id)

    #endregion

    # region Hardware Event Handlers

    def onTouchStart(self):
        pass

    def onTouchEnd(self):
        pass

    def onMove(self, value):
        setfiltervalue.onActionExecuteSlider(self, setfiltervalue.mapHardwareToValue(self, value))

    # endregion
