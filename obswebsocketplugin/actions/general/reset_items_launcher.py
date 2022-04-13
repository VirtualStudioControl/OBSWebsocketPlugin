from obswebsocketplugin.actions.general.triggerhotkey.trigger_hotkey_button import ButtonTriggerHotkey
from obswebsocketplugin.actions.general.triggerhotkey.trigger_hotkey_image_button import ImageButtonTriggerHotkey
from obswebsocketplugin.common.pluginloader import ROOT_DIRECTORY
from virtualstudio.common.action_manager.actionmanager import registerCategoryIcon
from virtualstudio.common.io import filewriter
from virtualstudio.common.structs.action.action_launcher import *
from virtualstudio.common.tools import icontools
from virtualstudio.common.tools.icontools import readPNGIcon


class TriggerHotkeyLauncher(ActionLauncher):

    def __init__(self):
        super(TriggerHotkeyLauncher, self).__init__()
        registerCategoryIcon(["OBS Websocket"], ROOT_DIRECTORY + "/assets/icons/category/obs_ws.png")
        registerCategoryIcon(["OBS Websocket", "General"], ROOT_DIRECTORY + "/assets/icons/category/obs_ws_general.png")

        self.ACTIONS = {
            #CONTROL_TYPE_BUTTON: ButtonTriggerHotkey,
            #CONTROL_TYPE_FADER: FaderSetFilterValue,
            #CONTROL_TYPE_IMAGE_BUTTON: ImageButtonTriggerHotkey,
            #CONTROL_TYPE_ROTARY_ENCODER: RotarySetFilterValue
        }

    #region Metadata

    def getName(self):
        return "Reset Scene Items"

    def getIcon(self):
        return readPNGIcon(ROOT_DIRECTORY + "/assets/icons/actions/general/reset_items.png")

    def getCategory(self):
        return ["OBS Websocket", "General"]

    def getAuthor(self):
        return "eric"

    def getVersion(self):
        return (0,0,1)

    def getActionStateCount(self, controlType: str) -> int:
        return 1

    def getActionUI(self, controlType: str) -> Tuple[str, str]:
        return UI_TYPE_QTUI, \
               icontools.encodeIconData(
                   filewriter.readFileBinary(ROOT_DIRECTORY + "/assets/ui/actions/general/reset_scene_items.ui"))
    #endregion