from libwsctrl.protocols.obs_ws5 import requests
from libwsctrl.protocols.obs_ws5.constants import hotkeys
from obswebsocketplugin.common.connection_manager import connection_manager
from obswebsocketplugin.common.uitools import setAccountComboBox, ensureAccountComboBox
from virtualstudio.common.account_manager import account_manager
from virtualstudio.common.logging import logengine
from virtualstudio.common.structs.action.imagebutton_action import ImageButtonAction


logger = logengine.getLogger()

ACCOUNT_COMBO = "account_combo"

SHORTCUT_TYPE_SELECT = "shortcut_type_select"

KEY_NAME_COMBO = "keyNameCombo"
CHECK_MOD_SHIFT = "hotkey_shift_check"
CHECK_MOD_ALT = "hotkey_alt_check"
CHECK_MOD_CONTROL = "hotkey_control_check"
CHECK_MOD_COMMAND = "hotkey_command_check"

SHORTCUT_NAME_EDIT = "shortcut_name_edit"


class ImageButtonTriggerHotkey(ImageButtonAction):

    #region handlers

    def onLoad(self):
        self.account_id = None
        self.uuid_map = []

    def onAppear(self):
        account_manager.registerAccountChangeCallback(self.accountChangedCB)
        self.uuid_map = ensureAccountComboBox(self, ACCOUNT_COMBO)
        index = self.getGUIParameter(ACCOUNT_COMBO, "currentIndex")
        if index is not None:
            self.account_id = self.uuid_map[index]
            self.initAccount(self.account_id)

        self.setGUIParameter(KEY_NAME_COMBO, "itemTexts", list(hotkeys.REVERSE_KEY_NAMES.keys()))

    def onDisappear(self):
        account_manager.unregisterAccountChangeCallback(self.accountChangedCB)
        index = self.getGUIParameter(ACCOUNT_COMBO, "currentIndex")
        if index is not None:
            self.account_id = self.uuid_map[index]
            self.deinitAccount(self.account_id)
            self.account_id = None

    def onSettingsGUIAppear(self):
        pass

    def onSettingsGUIDisappear(self):
        pass

    def onParamsChanged(self, parameters: dict):
        index = self.getGUIParameter(ACCOUNT_COMBO, "currentIndex")
        if index is not None:
            self.account_id = self.uuid_map[index]

    #endregion

    #region Action Management

    def initAccount(self, account_id):
        pass

    def deinitAccount(self, account_id):
        pass

    def accountChangedCB(self, uuid):
        if self.account_id is not None:
            self.deinitAccount(self.account_id)
            self.uuid_map = setAccountComboBox(self, "account_combo")
            index = self.getGUIParameter(ACCOUNT_COMBO, "currentIndex")
            if index is not None and index != uuid:
                self.account_id = self.uuid_map[index]
                self.initAccount(self.account_id)
    #endregion

    #region Hardware Event Handlers

    def onKeyDown(self):
        pass

    def onKeyUp(self):
        index = self.getGUIParameter(ACCOUNT_COMBO, "currentIndex")
        if index is not None:
            self.account_id = self.uuid_map[index]

            typeSelect = self.getGUIParameter(SHORTCUT_TYPE_SELECT, "currentIndex")

            if typeSelect == 0:
                shortcut = hotkeys.REVERSE_KEY_NAMES[self.getGUIParameter(KEY_NAME_COMBO, "currentText")]
                mods = {
                    'shift': self.getGUIParameter(CHECK_MOD_SHIFT, "checked"),
                    'alt': self.getGUIParameter(CHECK_MOD_ALT, "checked"),
                    'ctrl': self.getGUIParameter(CHECK_MOD_CONTROL, "checked"),
                    'cmd': self.getGUIParameter(CHECK_MOD_COMMAND, "checked")
                }
                logger.info("Sending Shortcut: {} with mods {}".format(shortcut, mods))
                logger.info("Trigger Hotkey Request: {}".format(requests.triggerHotkeyByKeySequence(shortcut, mods)))
                connection_manager.sendMessage(self.account_id, requests.triggerHotkeyByKeySequence(shortcut, mods))
            elif typeSelect == 1:
                connection_manager.sendMessage(self.account_id, requests.triggerHotkeyByName(
                    self.getGUIParameter(SHORTCUT_NAME_EDIT, "currentText")))
            else:
                logger.error("Invalid Tab Index. Are TriggerHotKey imeplementation and UI Synchronized ?")

    #endregion