from pathlib import Path
from typing import Any, Optional

from atomacos import NativeUIElement


class JobActionStates:
    def __init__(self):
        self.variables: dict[str, Any] = {}
        self.elements: dict[str, Optional[NativeUIElement]] = {}


class JobFileOutput:
    def __init__(self, root_dir: Path):
        self.root_dir = root_dir
