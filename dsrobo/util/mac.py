import re
import time
from typing import Optional

import atomacos.keyboard
import pyautogui
from atomacos import NativeUIElement

from dsrobo.util import center_of_rect, ElementIdentifier


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
        if re.fullmatch(name, title) is not None:
            return window

    return None


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
        elm_title = getattr(elm, 'AXTitle', '')
        if (title_ is not None) and (re.fullmatch(title_, elm_title) is None):
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
