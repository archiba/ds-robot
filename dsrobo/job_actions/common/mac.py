import time
from typing import Optional, Any

import atomacos
from atomacos import NativeUIElement
from pydantic import BaseModel, Field

from dsrobo.job_actions.base import JobActionBase
from dsrobo.job_actions.states import JobActionStates, JobFileOutput
from dsrobo.util import find_window_by_exact_name, ElementIdentifier, find_element_by_role_and_id, take_screenshot


class CommonTerminate(JobActionBase):
    name = "Terminate"

    class P(BaseModel):
        pass

    def _impl(self,
              states: JobActionStates,
              file_output: JobFileOutput,
              element: NativeUIElement,
              parameters: P) -> tuple[int, Any]:
        raise ValueError("Job is Terminated.")


class CommonFindWindow(JobActionBase):
    name = "FindWindow"

    class P(BaseModel):
        window_name: str
        dest_name: str

    def _impl(self,
              states: JobActionStates,
              file_output: JobFileOutput,
              element: NativeUIElement,
              parameters: P) \
            -> tuple[int, Optional[NativeUIElement]]:
        window = find_window_by_exact_name(
            element,
            parameters.window_name
        )
        states.elements[parameters.dest_name] = window
        return int(window is not None), window


class CommonFindElementByRole(JobActionBase):
    name = "FindElementByRole"

    class P(BaseModel):
        identifiers: list[ElementIdentifier]
        dest_name: str

    def _impl(self,
              states: JobActionStates,
              file_output: JobFileOutput,
              element: NativeUIElement,
              parameters: P) \
            -> tuple[int, Optional[NativeUIElement]]:
        for identifier in parameters.identifiers:
            element = find_element_by_role_and_id(
                element,
                identifier
            )
            if element is None:
                break

        states.elements[parameters.dest_name] = element
        return int(element is not None), element


class CommonTakeScreenshot(JobActionBase):
    name = "TakeScreenshot"

    class P(BaseModel):
        screenshot_name: str
        wait_seconds: float = Field(default=1, ge=0)

    def _impl(self,
              states: JobActionStates,
              file_output: JobFileOutput,
              element: NativeUIElement,
              parameters: P) \
            -> tuple[int, Optional[NativeUIElement]]:
        dest_path = file_output.root_dir / f"{parameters.screenshot_name}.png"
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        status = take_screenshot(element, str(dest_path))
        time.sleep(parameters.wait_seconds)
        return int(status), element


class CommonSendHotkey(JobActionBase):
    name = 'SendHotkey'

    class P(BaseModel):
        keys: list[str]
        wait_seconds: float = Field(default=1)

    def _impl(self,
              states: JobActionStates,
              file_output: JobFileOutput,
              element: NativeUIElement,
              parameters: P) \
            -> tuple[int, Optional[NativeUIElement]]:
        if hasattr(element, 'AXRaise'):
            element.AXRaise()
        atomacos.keyboard.hotkey(*parameters.keys)
        time.sleep(parameters.wait_seconds)
        return True, element


class CommonSendControl(JobActionBase):
    name = 'SendHotControl'

    class P(BaseModel):
        key: str
        press_duration: float = Field(default=1 / 30, ge=0)
        wait_seconds: float = Field(default=0.1, ge=0)

    def _impl(self,
              states: JobActionStates,
              file_output: JobFileOutput,
              element: NativeUIElement,
              parameters: P) \
            -> tuple[int, Optional[NativeUIElement]]:
        if hasattr(element, 'AXRaise'):
            element.AXRaise()
        atomacos.keyboard.keyDown(parameters.key)
        time.sleep(parameters.press_duration)
        atomacos.keyboard.keyUp(parameters.key)
        time.sleep(parameters.wait_seconds)
        return True, element


class CommonTypeWrite(JobActionBase):
    name = 'TypeWrite'

    class P(BaseModel):
        text: str
        wait_seconds: float = Field(default=5)

    def _impl(self,
              states: JobActionStates,
              file_output: JobFileOutput,
              element: NativeUIElement,
              parameters: P) \
            -> tuple[int, Optional[NativeUIElement]]:
        if hasattr(element, 'AXRaise'):
            element.AXRaise()
        atomacos.keyboard.typewrite(*parameters.text)
        time.sleep(parameters.wait_seconds)
        return True, element
