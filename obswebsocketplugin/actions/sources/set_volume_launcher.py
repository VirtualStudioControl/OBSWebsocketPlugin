from obswebsocketplugin.actions.sources.setvolume.button_setvolume import ButtonSetVolumeAction
from obswebsocketplugin.actions.sources.setvolume.fader_setvolume import FaderSetVolumeAction
from obswebsocketplugin.actions.sources.setvolume.imagebutton_setvolume import ImageButtonSetVolumeAction
from obswebsocketplugin.actions.sources.setvolume.rotary_setvolume import RotarySetVolumeAction
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
            CONTROL_TYPE_BUTTON: ButtonSetVolumeAction,
            CONTROL_TYPE_FADER: FaderSetVolumeAction,
            CONTROL_TYPE_IMAGE_BUTTON: ImageButtonSetVolumeAction,
            CONTROL_TYPE_ROTARY_ENCODER: RotarySetVolumeAction
        }

    #region Metadata

    def getName(self):
        return "Set Volume"

    def getIcon(self):
        return readPNGIcon(ROOT_DIRECTORY + "/assets/icons/actions/sources/audio_loud.png")

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
                   filewriter.readFileBinary(ROOT_DIRECTORY + "/assets/ui/actions/source/setvolume.ui"))
    #endregion