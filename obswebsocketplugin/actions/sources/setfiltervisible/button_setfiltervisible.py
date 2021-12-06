from typing import List, Dict, Optional

from libwsctrl.structs.callback import Callback
from obswebsocketplugin.actions.sources.setfiltervisible import setfiltervisible
from obswebsocketplugin.actions.sources.setfiltervisible.setfiltervisible import ACCOUNT_COMBO, SOURCENAME_COMBO, \
    FILTERNAME_COMBO, STATE_VISIBLE, STATE_INVISIBLE
from obswebsocketplugin.common.structs.obs_filter import OBSFilter
from obswebsocketplugin.common.uitools import setAccountComboBox
from virtualstudio.common.logging import logengine
from virtualstudio.common.structs.action.button_action import ButtonAction

logger = logengine.getLogger()

class ButtonSetFilterVisible(ButtonAction):

    #region handlers

    def onLoad(self):
        self.filterVisibilityChanged = Callback(self.onFilterVisibilityChanged)
        self.uuid_map = []
        self.account_id = None

        self.filters: Dict[str, OBSFilter] = {}
        self.filter: Optional[OBSFilter] = None

    def onAppear(self):
        setfiltervisible.onAppear(self)

    def onDisappear(self):
        setfiltervisible.onDisappear(self)

    def onSettingsGUIAppear(self):
        pass

    def onSettingsGUIDisappear(self):
        pass

    def onParamsChanged(self, parameters: dict):
        setfiltervisible.onParamsChanged(self, parameters)

    #endregion

    #region Action Management

    def accountChangedCB(self, uuid):
        if self.account_id is not None:
            setfiltervisible.deinitAccount(self, self.account_id)
            self.uuid_map = setAccountComboBox(self, "account_combo")
            index = self.getGUIParameter(ACCOUNT_COMBO, "currentIndex")
            if index is not None and index != uuid:
                self.account_id = self.uuid_map[index]
                setfiltervisible.initAccount(self, self.account_id)

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

    def updateFilters(self, msg, currentSelection: str = ""):
        if msg['status'] != 'ok':
            self.logger.error("Failed to retrieve scene list !" + str(msg))
            return

        filterNames = []
        if currentSelection is not None:
            filterNames.append(currentSelection)

        for filter in msg['filters']:
            if filter['name'] not in filterNames:
                filterNames.append(filter['name'])

            self.filters[filter['name']] = OBSFilter(enabled=filter['enabled'], name=filter['name'],
                                                     type=filter['type'], settings=filter['settings'])

        if self.getGUIParameter(FILTERNAME_COMBO, "currentText") not in filterNames and len(filterNames) > 0:
            self.setGUIParameter(FILTERNAME_COMBO, "currentIndex", 0, silent=True)
            self.setGUIParameter(FILTERNAME_COMBO, "currentText", filterNames[0], silent=True)
        else:
            self.setGUIParameter(FILTERNAME_COMBO, "currentIndex", filterNames.index(self.getGUIParameter(FILTERNAME_COMBO, "currentText")), silent=True)
        self.setGUIParameter(FILTERNAME_COMBO, "itemTexts", filterNames)

        if self.getGUIParameter(FILTERNAME_COMBO, "currentText")  is not None and self.getGUIParameter(FILTERNAME_COMBO, "currentText")  in self.filters:
            self.filter = self.filters[self.getGUIParameter(FILTERNAME_COMBO, "currentText")]
            self.updateState()

    def setMuteState(self, msg):
        if msg['status'] != 'ok':
            self.logger.error("Failed to retrieve mute state !" + str(msg))
            return
        if msg['name'] == self.getGUIParameter(SOURCENAME_COMBO, "currentText"):
            self.isMute = msg['muted']
            self.updateState()

    def onFilterVisibilityChanged(self, msg):
        if msg['sourceName'] == self.getGUIParameter(SOURCENAME_COMBO, "currentText"):
            if msg['filterName'] == self.filter.name:
                self.filter.enabled = msg['filterEnabled']
                self.updateState()

    def updateState(self):
        if self.filter is None:
            self.setState(STATE_INVISIBLE)
            return

        if self.filter.enabled:
            self.setState(STATE_VISIBLE)
        else:
            self.setState(STATE_INVISIBLE)

    #endregion

    #region Hardware Event Handlers

    def onKeyDown(self):
        pass

    def onKeyUp(self):
        setfiltervisible.onActionExecute(self)
        self.ensureLEDState()
    #endregion