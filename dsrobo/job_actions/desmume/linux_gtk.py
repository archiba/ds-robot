import time
from typing import Any

from pyatspi import Accessible
from pydantic import BaseModel, Field

from dsrobo.job_actions.base import JobActionBase
from dsrobo.job_actions.states import JobActionStates, JobFileOutput
from dsrobo.util.linux_gtk import click, open_file_using_ctrl_a
from dsrobo.util.linux_gtk import find_element_by_role_and_id, ElementIdentifier


class DeSmuMEReset(JobActionBase):
    name = 'Reset'

    class P(BaseModel):
        wait_seconds: float = Field(default=1., ge=0)

    def _impl(self,
              states: JobActionStates,
              file_output: JobFileOutput,
              element: Accessible,
              parameters: P) -> tuple[int, Any]:
        if element.getRoleName() != 'menu bar':
            print('The Element for DeSmuMEReset should be menu bar.')
            return False, element

        file_menu = find_element_by_role_and_id(element, ElementIdentifier(role="menu", name="File"))
        if file_menu is None:
            print("Could not find menu File")
            return False, file_menu
        reset_item = find_element_by_role_and_id(file_menu, ElementIdentifier(role="menu item", title="Reset"))
        if reset_item is None:
            print("Could not find menu item Reset")
            return False, reset_item
        click_result = click(reset_item)
        if not click_result:
            print("Could not click Reset button")
            return False, reset_item
        time.sleep(parameters.wait_seconds)
        return True, reset_item


class DeSmuMESaveStateFile(JobActionBase):
    name = 'SaveStateFile'

    class P(BaseModel):
        save_name: str = Field(default='state.dst')
        dialog_name: str = Field(default='.*')
        wait_seconds_after_click_save_state_to: float = Field(default=0.5, ge=0)
        wait_seconds_after_ctrl_a: float = Field(default=0.5, ge=0)
        wait_seconds_after_type_path: float = Field(default=0.5, ge=0)
        wait_seconds_after_first_enter: float = Field(default=0.5, ge=0)
        wait_seconds_after_second_enter: float = Field(default=0.5, ge=0)

    def _impl(self,
              states: JobActionStates,
              file_output: JobFileOutput,
              element: Accessible,
              parameters: P) -> tuple[int, Any]:
        dest_path = file_output.root_dir / parameters.save_name
        dest_path.parent.mkdir(parents=True, exist_ok=True)

        if element.getRoleName() != 'menu bar':
            print('DeSmuMESaveStateFile requires that input is menu bar.')
            return False, element

        file_menu = find_element_by_role_and_id(element, ElementIdentifier(role="menu", name="File"))
        if file_menu is None:
            print('Could not find menu File')
            return False, file_menu
        save_state_to_item = find_element_by_role_and_id(file_menu,
                                                         ElementIdentifier(role="menu item", title="Save state to.*"))
        if save_state_to_item is None:
            print("Could not find menu item Save state to")
            return False, save_state_to_item
        click_result = click(save_state_to_item)
        if not click_result:
            print("Could not click Save state button")
            return False, save_state_to_item
        time.sleep(parameters.wait_seconds_after_click_save_state_to)

        status = open_file_using_ctrl_a(
            element,
            parameters.dialog_name,
            str(dest_path),
            parameters.wait_seconds_after_ctrl_a,
            parameters.wait_seconds_after_type_path,
            parameters.wait_seconds_after_first_enter,
            parameters.wait_seconds_after_second_enter
        )

        run_item = find_element_by_role_and_id(file_menu, ElementIdentifier(role="menu item", title="Run"))
        if run_item is None:
            print("Could not find menu item Run")
            return False, run_item
        click_result = click(run_item)
        if not click_result:
            print("Could not click Run button")
            return False, run_item

        return status, element
