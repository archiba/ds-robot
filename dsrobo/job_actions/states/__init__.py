from pathlib import Path

from dsrobo.env import OS_GUI_NAME


class JobFileOutput:
    def __init__(self, root_dir: Path):
        self.root_dir = root_dir


if OS_GUI_NAME == 'MacOS':
    from .mac import JobActionStates as JobActionStatesMacOS

    JobActionStates = JobActionStatesMacOS
elif OS_GUI_NAME == 'LinuxGTK':
    from .linux_gtk import JobActionStates as JobActionStatesLinuxGTK

    JobActionStates = JobActionStatesLinuxGTK
