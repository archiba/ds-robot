import time
from pathlib import Path
from typing import Optional

import atomacos.keyboard
import pyautogui
from atomacos import NativeUIElement
from pydantic import BaseModel, Field


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


def center_of_element(element: NativeUIElement, safe: bool = True):
    rect = getattr(element, "AXFrame", None)
    if safe and (rect is None):
        return
    return center_of_rect(rect)


def find_window_by_exact_name(application: NativeUIElement, name: str) -> Optional[NativeUIElement]:
    role = getattr(application, "AXRole", "?")
    if role != "AXApplication":
        return None

    windows = getattr(application, "AXWindows", [])
    for window in windows:
        title = getattr(window, "AXTitle", "")
        if title == name:
            return window

    return None


class ElementIdentifier(BaseModel):
    role: str
    idx: int = Field(default=0)
    identifier: Optional[str] = None
    title: Optional[str] = None


def find_element_by_role_and_id(parent: NativeUIElement,
                                identifier: ElementIdentifier) -> Optional[NativeUIElement]:
    found_results = []
    for elm in getattr(parent, 'AXChildren', []):
        if getattr(elm, 'AXRole', '') != identifier.role:
            continue
        id_ = identifier.identifier
        if (id_ is not None) and (getattr(elm, 'AXIdentifier', '') != id_):
            continue
        title_ = identifier.title
        if (title_ is not None) and (getattr(elm, 'AXTitle', '') != title_):
            continue
        found_results.append(elm)
    idx = identifier.idx
    if len(found_results) <= idx:
        return None
    return found_results[idx]


def open_file_using_cmd_shift_g(
        application: NativeUIElement,
        dialog_name: str,
        file_path: str,
        wait_seconds_after_cmd_shift_g: float = 1,
        wait_seconds_after_type_path: float = 5,
        wait_seconds_after_press_first_enter: float = 1,
        wait_seconds_after_press_second_enter: float = 1) \
        -> bool:
    file_open_dialog = find_window_by_exact_name(application, dialog_name)
    if file_open_dialog is None:
        return False
    file_open_dialog.AXRaise()
    atomacos.keyboard.hotkey('command', 'shift', 'g')
    time.sleep(wait_seconds_after_cmd_shift_g)

    sheet = find_element_by_role_and_id(file_open_dialog,
                                        ElementIdentifier(role='AXSheet'))
    text_field = find_element_by_role_and_id(sheet,
                                             ElementIdentifier(role='AXTextField'))
    # atomacos.keyboard.typewrite(file_path)
    text_field.AXValue = file_path
    time.sleep(wait_seconds_after_type_path)

    atomacos.keyboard.hotkey('enter')
    time.sleep(wait_seconds_after_press_first_enter)

    atomacos.keyboard.hotkey('enter')
    time.sleep(wait_seconds_after_press_second_enter)

    file_open_dialog_ = find_window_by_exact_name(application, dialog_name)
    if file_open_dialog_ is not None:
        return False
    return True


def take_screenshot(window: NativeUIElement, dest_path: str) -> bool:
    if getattr(window, 'AXRole', '') != "AXWindow":
        return False
    frame = getattr(window, 'AXFrame', None)
    if frame is None:
        return False
    response = pyautogui.screenshot(
        None,
        region=(int(frame.x), int(frame.y), int(frame.width), int(frame.height))
    )
    response.save(dest_path)
    if response is None:
        return False
    return True
