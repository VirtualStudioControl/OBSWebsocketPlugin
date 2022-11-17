from pathlib import Path
from typing import List

from virtualstudio.common.account_manager.account_manager import registerAccountType

ROOT_DIRECTORY = str(Path(__file__).resolve().parents[2])

ACCOUNT_TYPE_WEBSOCKET5: str = "OBS Websocket 5.x"

ACCOUNT_TYPES: List[str] = [ACCOUNT_TYPE_WEBSOCKET5]

def initializePlugin():
    registerAccountType(ACCOUNT_TYPE_WEBSOCKET5, ROOT_DIRECTORY + "/assets/icons/category/obs_ws5.png")

initializePlugin()