from pathlib import Path
from typing import Optional

from pydantic import BaseModel, Field

from dsrobo.env import OS_GUI_NAME


def get_rom_abspath(rom_directory: Optional[str], rom_path: str) -> tuple[str, bool]:
    p = Path(rom_path)
    if p.is_absolute():
        return str(p.resolve()), p.exists()
    if rom_directory is None:
        rom_directory = ""
    rom_dir = Path(rom_directory)
    p = rom_dir / rom_path
    return str(p.resolve()), p.exists()


def center_of_rect(cg_rect) -> tuple[float, float]:
    return \
        cg_rect.x + cg_rect.width / 2, \
        cg_rect.y + cg_rect.height / 2


class ElementIdentifier(BaseModel):
    role: str
    idx: int = Field(default=0)
    identifier: Optional[str] = None
    title: Optional[str] = None


if OS_GUI_NAME == "MacOS":
    from .mac import (
        center_of_element,
        find_window_by_exact_name,
        find_element_by_role_and_id,
        open_file_using_cmd_shift_g,
        take_screenshot
    )
elif OS_GUI_NAME == "LinuxGTK":
    from .linux_gtk import (
        center_of_element,
        find_window_by_exact_name,
        find_element_by_role_and_id,
        open_file_using_ctrl_l,
        take_screenshot
    )
