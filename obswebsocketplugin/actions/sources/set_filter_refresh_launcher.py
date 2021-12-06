from obswebsocketplugin.actions.sources.setfilterrefresh.button_filterrefresh import ButtonFilterRefreshAction
from obswebsocketplugin.actions.sources.setfilterrefresh.imagebutton_filterrefresh import ImageButtonFilterRefreshAction
from obswebsocketplugin.common.pluginloader import ROOT_DIRECTORY
from virtualstudio.common.action_manager.actionmanager import registerCategoryIcon
from virtualstudio.common.io import filewriter
from virtualstudio.common.structs.action.action_launcher import *
from virtualstudio.common.tools import icontools
from virtualstudio.common.tools.icontools import readPNGIcon


class SetCurrentSceneLauncher(ActionLauncher):

    def __init__(self):
        super(SetCurrentSceneLauncher, self).__init__()
        registerCategoryIcon(["OBS Websocket"], ROOT_DIRECTORY + "/assets/icons/category/obs_ws.png")
        registerCategoryIcon(["OBS Websocket", "Sources"], ROOT_DIRECTORY + "/assets/icons/category/obs_ws_source.png")

        self.ACTIONS = {
            CONTROL_TYPE_BUTTON: ButtonFilterRefreshAction,
            #CONTROL_TYPE_FADER: FaderSetFilterValue,
            CONTROL_TYPE_IMAGE_BUTTON: ImageButtonFilterRefreshAction,
            #CONTROL_TYPE_ROTARY_ENCODER: RotarySetFilterValue
        }

    #region Metadata

    def getName(self):
        return "Filter Value Refresh"

    def getIcon(self):
        return readPNGIcon(ROOT_DIRECTORY + "/assets/icons/actions/sources/filter_refresh.png")

    def getCategory(self):
        return ["OBS Websocket", "Sources"]

    def getAuthor(self):
        return "eric"

    def getVersion(self):
        return (0,0,1)

    def getActionStateCount(self, controlType: str) -> int:
        return 1

    def getActionUI(self, controlType: str) -> Tuple[str, str]:
        return UI_TYPE_QTUI, \
               icontools.encodeIconData(
                   filewriter.readFileBinary(ROOT_DIRECTORY + "/assets/ui/actions/source/none.ui"))
    #endregion