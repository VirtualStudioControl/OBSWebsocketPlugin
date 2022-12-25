from libwsctrl.protocols.obs_ws5 import requests
from libwsctrl.protocols.obs_ws5 import events
from libwsctrl.structs.callback import Callback

from obswebsocketplugin.common.connection_manager import connection_manager
from obswebsocketplugin.common.uitools import ensureAccountComboBox
from virtualstudio.common.account_manager import account_manager
from virtualstudio.common.logging import logengine

ACCOUNT_COMBO = "account_combo"
SOURCENAME_COMBO = "sourcename_combo"
FILTERNAME_COMBO = "filtername_combo"

STATE_INVISIBLE = 0x0
STATE_VISIBLE = 0x1

logger = logengine.getLogger()

def onAppear(action):
    account_manager.registerAccountChangeCallback(action.accountChangedCB)
    action.uuid_map = ensureAccountComboBox(action, ACCOUNT_COMBO)
    index = action.getGUIParameter(ACCOUNT_COMBO, "currentIndex")
    if index is not None:
        action.account_id = action.uuid_map[index]
        initAccount(action, action.account_id)


def initAccount(action, account_id):
    connection_manager.sendMessage(account_id, requests.getInputList(),
                                   Callback(action.updateSources,
                                            currentSelection=action.getGUIParameter(SOURCENAME_COMBO, "currentText")))

    connection_manager.addEventListener(account_id, events.EVENT_SOURCEFILTERENABLESTATECHANGED, action.filterVisibilityChanged)
    source = action.getGUIParameter(SOURCENAME_COMBO, "currentText")
    if source is not None:
        connection_manager.sendMessage(action.account_id, requests.getSourceFilterList(source),
                                       Callback(action.updateFilters,
                                                currentSelection=action.getGUIParameter(FILTERNAME_COMBO,
                                                                                        "currentText")))


def deinitAccount(action, account_id):
    connection_manager.removeEventListener(account_id, events.EVENT_SOURCEFILTERENABLESTATECHANGED, action.filterVisibilityChanged)


def onDisappear(action):
    account_manager.unregisterAccountChangeCallback(action.accountChangedCB)
    index = action.getGUIParameter(ACCOUNT_COMBO, "currentIndex")
    if index is not None:
        action.account_id = action.uuid_map[index]
        deinitAccount(action, action.account_id)
        action.account_id = None


def onParamsChanged(action, parameters: dict):
    index = action.getGUIParameter(ACCOUNT_COMBO, "currentIndex")
    if index is not None:
        action.account_id = action.uuid_map[index]
        connection_manager.sendMessage(action.account_id, requests.getInputList(),
                                       Callback(action.updateSources,
                                                currentSelection=action.getGUIParameter(SOURCENAME_COMBO,
                                                                                        "currentText")))
        source = action.getGUIParameter(SOURCENAME_COMBO, "currentText")
        if source is not None:
            connection_manager.sendMessage(action.account_id, requests.getSourceFilterList(source),
                                       Callback(action.updateFilters,
                                                currentSelection=action.getGUIParameter(FILTERNAME_COMBO, "currentText")))

        filter = action.getGUIParameter(FILTERNAME_COMBO, "currentText")
        if filter is not None and filter in action.filters:
            action.filter = action.filters[filter]
            action.updateState()


def onActionExecute(action):
    index = action.getGUIParameter(ACCOUNT_COMBO, "currentIndex")
    if index is not None:
        account_id = action.uuid_map[index]
        if action.filter is not None:
            connection_manager.sendMessage(account_id, requests.setSourceFilterEnabled(action.getGUIParameter(SOURCENAME_COMBO, "currentText"),
                                                                                      action.filter.name, not action.filter.enabled))
        else:
            logger.warning("Filter {} is None !".format(action.getGUIParameter(FILTERNAME_COMBO, "currentText")))