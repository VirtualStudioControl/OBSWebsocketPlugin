from typing import List, Optional

from obswebsocketplugin.common.pluginloader import ACCOUNT_TYPES
from virtualstudio.common.account_manager import account_manager
from virtualstudio.common.logging import logengine
from virtualstudio.common.structs.action.abstract_action import AbstractAction

logger = logengine.getLogger()

def ensureAccountComboBox(action: AbstractAction, comboBoxName: str) -> List[str]:
    accounts = account_manager.getAccountListOfTypes(*ACCOUNT_TYPES)
    accountNames = [account.accountTitle for account in accounts]
    accountUUIDs: List[str] = [account.uuid for account in accounts]

    logger.debug(accountNames)

    action.ensureGUIParameter(comboBoxName, "itemTexts", accountNames)

    return accountUUIDs


def setAccountComboBox(action: AbstractAction, comboBoxName: str) -> List[str]:
    accounts = account_manager.getAccountListOfTypes(*ACCOUNT_TYPES)
    accountNames = [account.accountTitle for account in accounts]
    accountUUIDs: List[str] = [account.uuid for account in accounts]

    action.setGUIParameter(comboBoxName, "itemTexts", accountNames)

    return accountUUIDs