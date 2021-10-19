from obswebsocketplugin.actions.scenes.transition.button_transition import ButtonTransitionAction
from obswebsocketplugin.actions.scenes.transition.imagebutton_transition import ImageButtonTransitionAction
from obswebsocketplugin.common.pluginloader import ROOT_DIRECTORY

from virtualstudio.common.action_manager.actionmanager import registerCategoryIcon
from virtualstudio.common.io import filewriter
from virtualstudio.common.structs.action.action_launcher import *
from virtualstudio.common.tools import icontools
from virtualstudio.common.tools.icontools import readPNGIcon

from pathlib import Path

class TransitionLauncher(ActionLauncher):

    def __init__(self):
        super(TransitionLauncher, self).__init__()
        registerCategoryIcon(["OBS Websocket"], ROOT_DIRECTORY + "/assets/icons/category/obs_ws.png")
        registerCategoryIcon(["OBS Websocket", "Scenes"], ROOT_DIRECTORY + "/assets/icons/category/obs_ws_scene.png")

        self.ACTIONS = {
            CONTROL_TYPE_BUTTON: ButtonTransitionAction,
            #CONTROL_TYPE_FADER: FaderDebugAction,
            CONTROL_TYPE_IMAGE_BUTTON: ImageButtonTransitionAction,
            #CONTROL_TYPE_ROTARY_ENCODER: RotaryEncoderDebugAction
        }

    #region Metadata

    def getName(self):
        return "Transition"

    def getIcon(self):
        return readPNGIcon(ROOT_DIRECTORY + "/assets/icons/actions/scene/transition.png")

    def getCategory(self):
        return ["OBS Websocket", "Scenes"]

    def getAuthor(self):
        return "eric"

    def getVersion(self):
        return (0,0,1)

    def getActionStateCount(self, controlType: str) -> int:
        return 2

    def getActionUI(self, controlType: str) -> Tuple[str, str]:
        return UI_TYPE_QTUI, \
               icontools.encodeIconData(
                   filewriter.readFileBinary(ROOT_DIRECTORY + "/assets/ui/actions/scene/transition.ui"))
    #endregion