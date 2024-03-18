import logging
from typing import Any

from atomacos import NativeUIElement
from pydantic import BaseModel

from dsrobo.job_actions.states import JobActionStates, JobFileOutput

logger = logging.getLogger('job_actions')


class JobActionBase:
    name = "Base"

    class P(BaseModel):
        pass

    return_codes = {0, 1}

    def check_app_alive(self, application: NativeUIElement):
        logger.info('Checking the application availability.')
        if not hasattr(application, 'AXRole'):
            logger.error('Application is no longer available.')
            logger.error('Terminating...')
            raise ValueError('Application availability check failed error.')

    def validate(self,
                 parameters: dict[str, Any],
                 return_conditions: list[int]):
        self.__class__.P.parse_obj(parameters)
        return_codes = self.__class__.return_codes
        for c in return_conditions:
            if c not in return_codes:
                raise ValueError(f"Invalid return code {c}.")

    def __call__(self,
                 states: JobActionStates,
                 file_output: JobFileOutput,
                 application: NativeUIElement,
                 element: NativeUIElement,
                 parameters: dict[str, Any]) \
            -> tuple[int, Any]:
        params = self.__class__.P.parse_obj(parameters)
        self.check_app_alive(application)
        return self._impl(states, file_output, element, params)

    def _impl(self,
              states: JobActionStates,
              file_output: JobFileOutput,
              element: NativeUIElement,
              parameters: P) \
            -> tuple[int, Any]:
        raise NotImplementedError()
