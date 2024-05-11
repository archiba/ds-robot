from enum import Enum
from typing import Optional

from pydantic import Field, BaseModel

from dsrobo.env import OS_GUI_NAME

if OS_GUI_NAME == 'MacOS':
    from .mac import Config as ConfigMacOS
    Config = ConfigMacOS
elif OS_GUI_NAME == 'LinuxGTK':
    from .linux_gtk import Config as ConfigLinuxGTK
    Config = ConfigLinuxGTK


class EmulatorTypes(str, Enum):
    NintendoDS = 'nds'
    Nintendo3DS = '3ds'


class AvailableJobActions(str, Enum):
    Terminate = 'Terminate'
    FindWindow = 'FindWindow'
    FindElementByRole = 'FindElementByRole'
    TakeScreenshot = 'TakeScreenshot'
    SendHotkey = 'SendHotkey'
    SendHotControl = 'SendHotControl'
    TypeWrite = 'TypeWrite'
    Reset = 'Reset'
    SaveStateFile = 'SaveStateFile'


class JobActionConfig(BaseModel):
    action_name: str = Field(default='Untitled action')
    action_type: AvailableJobActions
    action_parameters: dict = Field(default={})
    target_element: str = Field(default='main_window')
    then: dict[int, list['JobActionConfig']] = Field(default={})
    wait_seconds_after_action: float = Field(default=300)
    n_repeats: Optional[int] = Field(default=None)


class JobConfig(BaseModel):
    job_name: str = Field(default="Untitled job")
    emulator_type: EmulatorTypes
    rom_file_path: str
    actions: list[JobActionConfig]
