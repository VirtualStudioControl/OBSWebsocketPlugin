import base64
from typing import List, Tuple, Union

from obswebsocketplugin.actions.general.resetsceneitems.resetsceneitems import ACCOUNT_COMBO, FILE_SELECTOR
from obswebsocketplugin.common.uitools import ensureAccountComboBox, setAccountComboBox
from virtualstudio.common.account_manager import account_manager
from virtualstudio.common.io.configtools import readJSON
from virtualstudio.common.logging import logengine
from virtualstudio.common.structs.action.imagebutton_action import ImageButtonAction

logger = logengine.getLogger()

class ImagebuttonResetSceneItemsAction(ImageButtonAction):

    #region handlers

    def onLoad(self):
        self.uuid_map = []
        self.account_id = ""

        self.filename = ""
        self.itemData = []

    def onAppear(self):
        account_manager.registerAccountChangeCallback(self.accountChangedCB)
        self.uuid_map = ensureAccountComboBox(self, ACCOUNT_COMBO)

        self.filename = self.getGUIParameter(FILE_SELECTOR, "currentFile")
        self.itemData = self.decodeSceneData(self.getGUIParameter(FILE_SELECTOR, "fileContent"))

        self.setGUIParameter(FILE_SELECTOR, "fileFilter", "DMXFrame (*.dmxframe)")

        index = self.getGUIParameter(ACCOUNT_COMBO, "currentIndex")
        if index is not None:
            self.account_id = self.uuid_map[index]
            self.initAccount()

    def initAccount(self):
        pass

    def onDisappear(self):
        pass

    def onSettingsGUIAppear(self):
        pass

    def onSettingsGUIDisappear(self):
        pass

    def onParamsChanged(self, parameters: dict):
        filename = self.getGUIParameter(FILE_SELECTOR, "currentFile")
        if self.filename != filename:
            self.filename = filename
            self.itemData = self.decodeSceneData(self.getGUIParameter(FILE_SELECTOR, "fileContent"))

        index = self.getGUIParameter(ACCOUNT_COMBO, "currentIndex")
        if index is not None:
            self.account_id = self.uuid_map[index]

    #endregion

    #region DMXFrame

    def decodeSceneData(self, base64data: str):
        if base64data is None:
            return None
        bindata = base64.b64decode(base64data.encode("utf-8"))
        return readJSON(bindata.decode("utf-8"))

    #endregion

    #region Action Management

    def accountChangedCB(self, uuid):
        if self.account_id is not None:
            self.uuid_map = setAccountComboBox(self, "account_combo")
            index = self.getGUIParameter(ACCOUNT_COMBO, "currentIndex")
            if index is not None and index != uuid:
                self.account_id = self.uuid_map[index]
                self.initAccount()

    #endregion

    # region Hardware Event Handlers

    def onKeyDown(self):
        pass

    def onKeyUp(self):
        if self.account_id == "":
            return

        if self.itemData is not None:
            pass
        else:
            logger.info("Scene Item Data is None !")

    # endregion
