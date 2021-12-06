from typing import Dict


class OBSFilter:

    def __init__(self, enabled: bool = False, type: str = "", name: str = "", settings=None):
        super(OBSFilter, self).__init__()

        if settings is None:
            settings = {}

        self.enabled: bool = enabled
        self.type: str = type
        self.name: str = name
        self.settings: Dict = settings