import re
import time
from typing import Optional, NamedTuple

import pyautogui
from pyatspi import Accessible, Component, Registry, KEY_PRESS, KEY_RELEASE, KEY_STRING, Action

from dsrobo.util import center_of_rect, ElementIdentifier


class Rect(NamedTuple):
    x: float
    y: float
    width: float
    height: float


def center_of_element(element: Accessible, safe: bool = True):
    try:
        rect = Component(element).getExtents(0)
    except:
        if not safe:
            raise
        return None
    return center_of_rect(Rect(*rect))


def find_window_by_exact_name(application: Accessible, name: str) -> Optional[Accessible]:
    role = application.getRoleName()
    if role != "application":
        return None

    for child in application:
        child_role = child.getRoleName()
        if child_role != "frame":
            continue
        if re.fullmatch(name, child.name) is not None:
            return child
    return None


def find_element_by_role_and_id(parent: Accessible,
                                identifier: ElementIdentifier) -> Optional[Accessible]:
    found_results = []
    for elm in parent:
        elm_role = elm.getRoleName()
        if elm_role != identifier.role:
            continue
        id_ = identifier.identifier
        elm_id = elm.accessibleId
        if (id_ is not None) and (elm_id != id_):
            continue
        title_ = identifier.title
        elm_title = elm.name
        if (title_ is not None) and (re.fullmatch(title_, elm_title) is None):
            continue
        found_results.append(elm)
    idx = identifier.idx
    if len(found_results) <= idx:
        return None
    return found_results[idx]


def send_keys(registry: Registry, key_codes: list[int]):
    """
    # Key code cheat sheet:
    Z: 52
    X: 53
    A: 38
    S: 39
    Q: 24
    W: 25
    Space: 65
    Left Arrow: 113
    Right Arrow: 114
    Up Arrow: 111
    Down Arrow: 116
    Ctrl: 38

    # Default DeSmuME key mapping:
    Z(52) = B
    X(53) = A
    A(38) = Y
    S(39) = X
    Q(24) = L
    W(25) = R
    ENTER(36)= START
    SPACE(65)= SELECT
    MOUSE= TOUCHSCREEN

    """
    for key_code in key_codes:
        registry.generateKeyboardEvent(key_code, None, KEY_PRESS)
    for key_code in key_codes[::-1]:
        registry.generateKeyboardEvent(key_code, None, KEY_RELEASE)


def press_key(registry: Registry, key_code: int, press_duration: float):
    registry.generateKeyboardEvent(key_code, None, KEY_PRESS)
    time.sleep(press_duration)
    registry.generateKeyboardEvent(key_code, None, KEY_RELEASE)


def type_write(registry: Registry, text: str):
    registry.generateKeyboardEvent(0, text, KEY_STRING)


def try_to_run_action(element: Accessible, action: str) -> bool:
    try:
        action_obj: Optional[Action] = element.queryAction()
        if action_obj is None:
            print(f"Element {element} is not actionable accessible.")
            return False
        for i in range(action_obj.nActions):
            if action_obj.getName(i) == action:
                action_obj.doAction(i)
                return True
        return False
    except Exception as e:
        print(f"Failed to run a action {action} on element {element}.")
        print(e)
        return False


def click(element: Accessible) -> bool:
    return try_to_run_action(element, "click")


def open_file_using_keys(
        application: Accessible,
        dialog_name: str,
        file_path: str,
        keys: list[int],
        wait_seconds_after_keys: float = 1,
        wait_seconds_after_type_path: float = 5,
        wait_seconds_after_press_first_enter: float = 1,
        wait_seconds_after_press_second_enter: float = 0) \
        -> bool:
    registry = Registry()
    send_keys(registry, keys)  # CTRL + L
    time.sleep(wait_seconds_after_keys)

    registry.generateKeyboardEvent(0, file_path, KEY_STRING)
    time.sleep(wait_seconds_after_type_path)

    send_keys(registry, [36])
    time.sleep(wait_seconds_after_press_first_enter)
    time.sleep(wait_seconds_after_press_second_enter)

    return True


def open_file_using_ctrl_l(
        application: Accessible,
        dialog_name: str,
        file_path: str,
        wait_seconds_after_ctrl_l: float = 1,
        wait_seconds_after_type_path: float = 5,
        wait_seconds_after_press_first_enter: float = 1,
        wait_seconds_after_press_second_enter: float = 0):
    return open_file_using_keys(application, dialog_name, file_path, [37, 46],
                                wait_seconds_after_ctrl_l, wait_seconds_after_type_path,
                                wait_seconds_after_press_first_enter, wait_seconds_after_press_second_enter)


def open_file_using_ctrl_a(
        application: Accessible,
        dialog_name: str,
        file_path: str,
        wait_seconds_after_ctrl_a: float = 1,
        wait_seconds_after_type_path: float = 5,
        wait_seconds_after_press_first_enter: float = 1,
        wait_seconds_after_press_second_enter: float = 0):
    return open_file_using_keys(application, dialog_name, file_path, [37, 38],
                                wait_seconds_after_ctrl_a, wait_seconds_after_type_path,
                                wait_seconds_after_press_first_enter, wait_seconds_after_press_second_enter)


def take_screenshot(window: Accessible, dest_path: str) -> bool:
    role = window.getRoleName()
    if role != "frame":
        print("Should pass frame to take_screenshot.")
        return False
    rect = Component(window).getExtents(0)
    frame = Rect(*rect)
    response = pyautogui.screenshot(
        None,
        region=(int(frame.x), int(frame.y), int(frame.width), int(frame.height))
    )
    response.save(dest_path)
    if response is None:
        print("Failed to take screenshot with unknown reason.")
        return False
    return True
