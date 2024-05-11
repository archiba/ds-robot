from typing import Any, Optional

from pyatspi import Accessible


class JobActionStates:
    def __init__(self):
        self.variables: dict[str, Any] = {}
        self.elements: dict[str, Optional[Accessible]] = {}
