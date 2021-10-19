from obswebsocketplugin.actions.scenes.setcurrentscene.button_setcurrenscene import ButtonSetCurrentSceneAction
from obswebsocketplugin.actions.scenes.setcurrentscene.imagebutton_setcurrenscene import ImageButtonSetCurrentSceneAction
from obswebsocketplugin.common.pluginloader import ROOT_DIRECTORY

from virtualstudio.common.action_manager.actionmanager import registerCategoryIcon
from virtualstudio.common.io import filewriter
from virtualstudio.common.structs.action.action_launcher import *
from virtualstudio.common.tools import icontools
from virtualstudio.common.tools.icontools import readPNGIcon

from pathlib import Path

class SetCurrentSceneLauncher(ActionLauncher):

    def __init__(self):
        super(SetCurrentSceneLauncher, self).__init__()
        registerCategoryIcon(["OBS Websocket"], ROOT_DIRECTORY + "/assets/icons/category/obs_ws.png")
        registerCategoryIcon(["OBS Websocket", "Scenes"], ROOT_DIRECTORY + "/assets/icons/category/obs_ws_scene.png")

        self.ACTIONS = {
            CONTROL_TYPE_BUTTON: ButtonSetCurrentSceneAction,
            #CONTROL_TYPE_FADER: FaderDebugAction,
            CONTROL_TYPE_IMAGE_BUTTON: ImageButtonSetCurrentSceneAction,
            #CONTROL_TYPE_ROTARY_ENCODER: RotaryEncoderDebugAction
        }

    #region Metadata

    def getName(self):
        return "Switch Scene"

    def getIcon(self):
        return readPNGIcon(ROOT_DIRECTORY + "/assets/icons/actions/scene/obs_ws_scene.png")

    def getCategory(self):
        return ["OBS Websocket", "Scenes"]

    def getAuthor(self):
        return "eric"

    def getVersion(self):
        return (0,0,1)

    def getActionStateCount(self, controlType: str) -> int:
        return 4

    def getActionUI(self, controlType: str) -> Tuple[str, str]:
        return UI_TYPE_QTUI, \
               icontools.encodeIconData(
                   filewriter.readFileBinary(ROOT_DIRECTORY + "/assets/ui/actions/scene/setcurrentscene.ui"))
    #endregion