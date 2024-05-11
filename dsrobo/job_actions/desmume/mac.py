import time
from typing import Any

import atomacos
from atomacos import NativeUIElement
from pydantic import BaseModel, Field

from dsrobo.job_actions.base import JobActionBase
from dsrobo.job_actions.states import JobActionStates, JobFileOutput
from dsrobo.util.mac import find_element_by_role_and_id, ElementIdentifier, open_file_using_cmd_shift_g


class DeSmuMEReset(JobActionBase):
    name = 'Reset'

    class P(BaseModel):
        wait_seconds: float = Field(default=1., ge=0)

    def _impl(self,
              states: JobActionStates,
              file_output: JobFileOutput,
              element: NativeUIElement,
              parameters: P) -> tuple[int, Any]:
        if getattr(element, 'AXRole', '') != 'AXMenuBar':
            return False, element
        emulation_menu = find_element_by_role_and_id(
            element,
            ElementIdentifier(
                role='AXMenuBarItem',
                title='Emulation'
            )
        )
        if emulation_menu is None:
            return False, emulation_menu
        menu = find_element_by_role_and_id(
            emulation_menu,
            ElementIdentifier(
                role='AXMenu'
            )
        )
        if menu is None:
            return False, menu
        reset_item = find_element_by_role_and_id(
            menu,
            ElementIdentifier(
                role='AXMenuItem',
                title='Reset'
            )
        )
        if reset_item is None:
            return False, reset_item
        if not hasattr(reset_item, 'AXPress'):
            return False, reset_item
        reset_item.AXPress()
        time.sleep(parameters.wait_seconds)
        return True, reset_item


class DeSmuMESaveStateFile(JobActionBase):
    name = 'SaveStateFile'

    class P(BaseModel):
        save_name: str = Field(default='state.dst')
        dialog_name: str = Field(default='Save State File')
        wait_seconds_after_command_shift_s: float = Field(default=0.5, ge=0)
        wait_seconds_after_command_shift_g: float = Field(default=0.5, ge=0)
        wait_seconds_after_type_path: float = Field(default=0.5, ge=0)
        wait_seconds_after_first_enter: float = Field(default=0.5, ge=0)
        wait_seconds_after_second_enter: float = Field(default=0.5, ge=0)

    def _impl(self,
              states: JobActionStates,
              file_output: JobFileOutput,
              element: NativeUIElement,
              parameters: P) -> tuple[int, Any]:
        dest_path = file_output.root_dir / parameters.save_name
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        if hasattr(element, 'AXRaise'):
            element.AXRaise()
        atomacos.keyboard.hotkey('command', 'shift', 's')
        time.sleep(parameters.wait_seconds_after_command_shift_s)
        status = open_file_using_cmd_shift_g(
            element,
            parameters.dialog_name,
            str(dest_path),
            parameters.wait_seconds_after_command_shift_g,
            parameters.wait_seconds_after_type_path,
            parameters.wait_seconds_after_first_enter,
            parameters.wait_seconds_after_second_enter
        )
        return status, element
