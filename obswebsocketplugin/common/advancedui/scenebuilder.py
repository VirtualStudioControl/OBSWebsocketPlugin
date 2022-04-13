from typing import List


class SceneBuilder:

    def __init__(self):
        self._current_sources: List[str] = []
        self._current_scene_name = ""

