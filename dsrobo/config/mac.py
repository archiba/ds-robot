from typing import Optional

from pydantic import Field, BaseModel


class DeSmuMEActionConfig(BaseModel):
    # launch section
    launch__after_launch_wait_seconds: float = Field(default=3., ge=0)
    launch__click_after_launch: bool = Field(default=True)
    launch__after_click_wait_seconds: float = Field(default=1., ge=0)
    launch__assert_focus_after_launch: bool = Field(default=True)

    # load_rom section
    load_rom__open_rom_dialog_name: str = Field(default='Open ROM')
    load_rom__before_cmd_shift_g_wait_seconds: float = Field(default=1., ge=0)
    load_rom__after_cmd_shift_g_wait_seconds: float = Field(default=1., ge=0)
    load_rom__after_type_path: float = Field(default=1., ge=0)
    load_rom__after_first_enter_wait_seconds: float = Field(default=1., ge=0)
    load_rom__after_second_enter_wait_seconds: float = Field(default=1., ge=0)
    load_rom__assert_rom_loaded: bool = Field(default=True)


class DeSmuMEConfig(BaseModel):
    application_path: str = Field(default="/Applications/DeSmuME.app")
    main_window_name: str = Field(default="DeSmuME")
    action: DeSmuMEActionConfig = Field(default=DeSmuMEActionConfig())


class CitraConfig(BaseModel):
    application_path: str = Field(default="/Applications/Citra/nightly/citra-qt.app")
    main_window_name: str = Field(default="Citra")


class Config(BaseModel):
    desmume: DeSmuMEConfig = Field(default=DeSmuMEConfig())
    citra: CitraConfig = Field(default=CitraConfig())
    rom_directory: Optional[str] = Field(default=None)
    dest_directory: Optional[str] = Field(default='artifacts')

