from libwsctrl.structs.callback import Callback
from obswebsocketplugin.common.connection_manager import connection_manager
from obswebsocketplugin.common.filter_data_manager import filter_data_manager
from obswebsocketplugin.common.structs.obs_filter import OBSFilter
from obswebsocketplugin.common.structs.obs_filter_setting_defaults import *
from obswebsocketplugin.common.uitools import ensureAccountComboBox
from virtualstudio.common.account_manager import account_manager
from virtualstudio.common.logging import logengine
from virtualstudio.common.structs.action.abstract_action import AbstractAction

from libwsctrl.protocols.obs_ws4 import obs_websocket_protocol as requests
from libwsctrl.protocols.obs_ws4 import obs_websocket_events as events

logger = logengine.getLogger()

ACCOUNT_COMBO = "account_combo"
SOURCE_NAME_COMBO = "sourcename_combo"
FILTER_NAME_COMBO = "filtername_combo"
FILTER_VALUE_COMBO = "filter_value_combo"

STACK_CONTROL = "stack_control"
PAGE_SLIDER = 0
PAGE_BUTTON = 1


PAGE_VALUE_NONE = 0
PAGE_VALUE_FLOAT = 1
PAGE_VALUE_INT = 2
PAGE_VALUE_COLOR = 3
PAGE_VALUE_BOOL = 4
PAGE_VALUE_STRING = 5
PAGE_VALUE_ENUM = 6

PAGE_MODE_SET = 0
PAGE_MODE_MODIFY = 1

CONTROL_TYPE_POSTFIX = ["slider", "button"]

VALUE_TYPE_POSTFIX = ["none", "float", "int", "color", "bool", "string", "enum"]

STACK_VALUETYPES_BASE = "stack_valuetypes"

BASE_PAGE_VALUE = "page_value"
BASE_MAPPING_COMBO = "mapping_combo"
BASE_VALUE_SPIN = "value_spin"
BASE_MAXIMUM_VALUE = "maximum_value_spin"
BASE_MINIMUM_VALUE = "minimum_value_spin"
BASE_STEP_SIZE = "stepsize_spin"
BASE_CHANNEL_COMBO = "channel_combo"
BASE_CUTOFF_SPIN = "cutoff_spin"

BASE_VALUE_BUTTON = "value_button"

BASE_VALUE_EDIT = "value_edit"
BASE_ALTVALUE_EDIT = "altvalue_edit"

BASE_MODE_COMBO = "mode_combo"


def getWidgetName(basename="", control_page=PAGE_SLIDER, value_type=PAGE_VALUE_FLOAT):
    return "{}_{}_{}".format(basename, VALUE_TYPE_POSTFIX[value_type], CONTROL_TYPE_POSTFIX[control_page])


def setActivePage(action: AbstractAction, control_page=PAGE_SLIDER, value_type=PAGE_VALUE_NONE):
    action.setGUIParameter(STACK_CONTROL, "currentIndex", control_page)
    action.setGUIParameter("{}_{}".format(STACK_VALUETYPES_BASE, CONTROL_TYPE_POSTFIX[control_page]),
                           "currentIndex", value_type)

#region Update UI Elements

def updateSources(action, msg, currentSelection: str = ""):
    if msg['status'] != 'ok':
        action.logger.error("Failed to retrieve scene list !" + str(msg))
        return

    sourceNames = []
    if currentSelection is not None:
        sourceNames.append(currentSelection)

    for source in msg['sources']:
        if source['name'] not in sourceNames:
            sourceNames.append(source['name'])

    if action.getGUIParameter(SOURCE_NAME_COMBO, "currentText") not in sourceNames and len(sourceNames) > 0:
        action.setGUIParameter(SOURCE_NAME_COMBO, "currentIndex", 0, silent=True)
        action.setGUIParameter(SOURCE_NAME_COMBO, "currentText", sourceNames[0], silent=True)
    else:
        action.setGUIParameter(SOURCE_NAME_COMBO, "currentIndex", sourceNames.index(action.getGUIParameter(SOURCE_NAME_COMBO, "currentText")), silent=True)
    action.setGUIParameter(SOURCE_NAME_COMBO, "itemTexts", sourceNames)

    connection_manager.sendMessage(action.account_id, requests.getSourceFilters(currentSelection),
                                   Callback(updateFilters,
                                            currentSelection=action.getGUIParameter(FILTER_NAME_COMBO,
                                                                                    "currentText"), action=action))


def updateFilters(action, msg, currentSelection: str = ""):
    if msg['status'] != 'ok':
        logger.error("Failed to retrieve filter list !" + str(msg))
        return

    filterNames = []
    if currentSelection is not None:
        filterNames.append(currentSelection)

    for filter in msg['filters']:
        if filter['name'] not in filterNames:
            filterNames.append(filter['name'])

        action.filters[filter['name']] = OBSFilter(enabled=filter['enabled'], name=filter['name'],
                                                 type=filter['type'], settings=filter['settings'])

    if action.getGUIParameter(FILTER_NAME_COMBO, "currentText") not in filterNames and len(filterNames) > 0:
        action.setGUIParameter(FILTER_NAME_COMBO, "currentIndex", 0, silent=True)
        action.setGUIParameter(FILTER_NAME_COMBO, "currentText", filterNames[0], silent=True)
    else:
        action.setGUIParameter(FILTER_NAME_COMBO, "currentIndex", filterNames.index(action.getGUIParameter(FILTER_NAME_COMBO, "currentText")), silent=True)
    action.setGUIParameter(FILTER_NAME_COMBO, "itemTexts", filterNames)

    if action.getGUIParameter(FILTER_NAME_COMBO, "currentText")  is not None and action.getGUIParameter(FILTER_NAME_COMBO, "currentText")  in action.filters:
        action.filter = action.filters[action.getGUIParameter(FILTER_NAME_COMBO, "currentText")]

        updateFilterParameters(action)


def updateFilterParameters(action):
    filterType = action.filter.type

    setting_names = list(getSettingsForType(filterType).keys())

    logger.info("{}: {}".format(filterType, setting_names))

    if action.getGUIParameter(FILTER_VALUE_COMBO, "currentText") not in setting_names and len(setting_names) > 0:
        action.setGUIParameter(FILTER_VALUE_COMBO, "currentIndex", 0, silent=True)
        action.setGUIParameter(FILTER_VALUE_COMBO, "currentText", setting_names[0], silent=True)
    elif len(setting_names) > 0:
        action.setGUIParameter(FILTER_VALUE_COMBO, "currentIndex", setting_names.index(action.getGUIParameter(FILTER_VALUE_COMBO, "currentText")), silent=True)
    action.setGUIParameter(FILTER_VALUE_COMBO, "itemTexts", setting_names)

    if action.getGUIParameter(FILTER_VALUE_COMBO, "currentText") is not None:
        updateFilterParamEditor(action)

def updateFilterParamEditor(action):
    filterType = action.filter.type
    filterSetting = action.getGUIParameter(FILTER_VALUE_COMBO, "currentText")


    settings = getSettingsForType(filterType)[filterSetting]

    if filterSetting not in action.filter.settings:
        action.filter.settings[filterSetting] = settings[VALUE_DESC_DEFAULT]

    action.value_type = settings[VALUE_DESC_TYPE]
    setActivePage(action, action.control_page, action.value_type)

    setMinMax(action, getWidgetName(BASE_MINIMUM_VALUE, action.control_page, action.value_type), settings[VALUE_DESC_MIN],
              settings[VALUE_DESC_MAX])

    setMinMax(action, getWidgetName(BASE_MAXIMUM_VALUE, action.control_page, action.value_type), settings[VALUE_DESC_MIN],
              settings[VALUE_DESC_MAX])

    setMinMax(action, getWidgetName(BASE_VALUE_SPIN, action.control_page, action.value_type), settings[VALUE_DESC_MIN],
              settings[VALUE_DESC_MAX])

    setMinMax(action, getWidgetName(BASE_STEP_SIZE, action.control_page, action.value_type), 0.000001,
              settings[VALUE_DESC_MAX] - settings[VALUE_DESC_MIN])

    action.updateHardware()


def setMinMax(action, widget, minimum, maximum):
    if minimum is None:
        minimum = - 2**32-1
    if maximum is None:
        maximum = 2**32-1

    action.setGUIParameter(widget, "maximum", maximum)
    action.setGUIParameter(widget, "minimum", minimum)


#endregion

def onLoad(action):

    action.prevuivals = {
        ACCOUNT_COMBO: "",
        SOURCE_NAME_COMBO: "",
        FILTER_NAME_COMBO: "",
        FILTER_VALUE_COMBO: "",
    }

def updateFilterValues(action):
    connection_manager.sendMessage(action.account_id,
                                   requests.getSourceFilters(action.getGUIParameter(SOURCE_NAME_COMBO, "currentText")),
                                   Callback(updateFilters,
                                            currentSelection=action.getGUIParameter(FILTER_NAME_COMBO,
                                                                                    "currentText"), action=action))


def updateUI(action):

    if action.getGUIParameter(ACCOUNT_COMBO, "currentText") != action.prevuivals[ACCOUNT_COMBO]:
        connection_manager.sendMessage(action.account_id, requests.getSourcesList(),
                                       Callback(updateSources,
                                                currentSelection=action.getGUIParameter(SOURCE_NAME_COMBO,
                                                                                        "currentText"), action=action))
    elif action.getGUIParameter(SOURCE_NAME_COMBO, "currentText") != action.prevuivals[SOURCE_NAME_COMBO]:
        connection_manager.sendMessage(action.account_id, requests.getSourceFilters(action.getGUIParameter(SOURCE_NAME_COMBO, "currentText")),
                                       Callback(updateFilters,
                                                currentSelection=action.getGUIParameter(FILTER_NAME_COMBO,
                                                                                        "currentText"), action=action))
    elif action.getGUIParameter(FILTER_NAME_COMBO, "currentText") != action.prevuivals[FILTER_NAME_COMBO]:
        updateFilterParameters(action)
    elif action.getGUIParameter(FILTER_VALUE_COMBO, "currentText") != action.prevuivals[FILTER_VALUE_COMBO]:
        updateFilterParamEditor(action)

    action.prevuivals = {
        ACCOUNT_COMBO: action.getGUIParameter(ACCOUNT_COMBO, "currentText"),
        SOURCE_NAME_COMBO: action.getGUIParameter(SOURCE_NAME_COMBO, "currentText"),
        FILTER_NAME_COMBO: action.getGUIParameter(FILTER_NAME_COMBO, "currentText"),
        FILTER_VALUE_COMBO: action.getGUIParameter(FILTER_VALUE_COMBO, "currentText"),
    }


def onAppear(action):
    filter_data_manager.addFilterDataAction(action)
    account_manager.registerAccountChangeCallback(action.accountChangedCB)
    action.uuid_map = ensureAccountComboBox(action, ACCOUNT_COMBO)
    index = action.getGUIParameter(ACCOUNT_COMBO, "currentIndex")
    if index is not None:
        action.account_id = action.uuid_map[index]
        initAccount(action, action.account_id)


def onDisappear(action):
    filter_data_manager.removeFilterDataAction(action)


def onParamsChanged(action, parameters):
    index = action.getGUIParameter(ACCOUNT_COMBO, "currentIndex")
    if index is not None:
        action.account_id = action.uuid_map[index]
        updateUI(action)


def initAccount(action, account_id):
    connection_manager.sendMessage(account_id, requests.getSourcesList(),
                                   Callback(updateSources,
                                            currentSelection=action.getGUIParameter(SOURCE_NAME_COMBO, "currentText"), action=action))

    #connection_manager.addEventListener(account_id, events.EVENT_SOURCEFILTERVISIBILITYCHANGED,
    #                                    action.filterVisibilityChanged)
#    source = action.getGUIParameter(SOURCE_NAME_COMBO, "currentText")
#    if source is not None:
#        connection_manager.sendMessage(action.account_id, requests.getSourceFilters(source),
#                                       Callback(action.updateFilters,
#                                                currentSelection=action.getGUIParameter(FILTER_NAME_COMBO,
#                                                                                        "currentText")))


def deinitAccount(self, account_id):
    return None


def mapHardwareToValue(action, value) -> float:
    minimum = action.getGUIParameter(getWidgetName(BASE_MINIMUM_VALUE, action.control_page, action.value_type), "value")
    maximum = action.getGUIParameter(getWidgetName(BASE_MAXIMUM_VALUE, action.control_page, action.value_type), "value")

    norm_val = float(value)/127.0

    return (norm_val * (maximum - minimum)) + minimum


def mapValueToHardware(action, value) -> int:
    minimum = action.getGUIParameter(getWidgetName(BASE_MINIMUM_VALUE, action.control_page, action.value_type), "value")
    maximum = action.getGUIParameter(getWidgetName(BASE_MAXIMUM_VALUE, action.control_page, action.value_type), "value")

    norm_val = float(value-minimum)/float(maximum - minimum)

    return max(min(int(norm_val * 127), 127), 0)


def onActionExecuteSlider(action, value):
    index = action.getGUIParameter(ACCOUNT_COMBO, "currentIndex")
    if index is not None:
        action.account_id = action.uuid_map[index]

        if action.value_type == VALUE_TYPE_FLOAT or action.value_type == VALUE_TYPE_INT:
            execute(action, value)

        elif action.value_type == VALUE_TYPE_COLOR:
            color_channel = action.getGUIParameter(getWidgetName(BASE_CHANNEL_COMBO, action.control_page, action.value_type), "currentIndex")

            if color_channel == 0:
                #red
                pass
            elif color_channel == 1:
                #green
                pass
            elif color_channel == 2:
                #blue
                pass
            elif color_channel == 3:
                #hue
                pass
            elif color_channel == 4:
                #saturation
                pass
            elif color_channel == 5:
                #value
                pass
            elif color_channel == 6:
                #alpha
                pass

        elif action.value_type == VALUE_TYPE_BOOLEAN:
            threshold = action.getGUIParameter(getWidgetName(BASE_CUTOFF_SPIN, action.control_page, action.value_type), "value")
            execute(action, value > threshold)

        #PAGE_VALUE_STRING = 5
        #PAGE_VALUE_ENUM = 6


def execute(action, value):
    source = action.getGUIParameter(SOURCE_NAME_COMBO, "currentText")
    filterName = action.getGUIParameter(FILTER_NAME_COMBO, "currentText")
    filterValueName = action.getGUIParameter(FILTER_VALUE_COMBO, "currentText")
    filterSettings = {}

    filterSettings[filterValueName] = value

    connection_manager.sendMessage(action.account_id, requests.setSourceFilterSettings(sourceName=source,
                                                                                       filterName=filterName,
                                                                                       filterSettings=filterSettings))