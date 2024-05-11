import time
from subprocess import Popen

import pyatspi
from pyatspi import Accessible, STATE_ACTIVE
import logging

from dsrobo.config import Config
from dsrobo.util.linux_gtk import find_window_by_exact_name
from dsrobo.util.linux_gtk import center_of_element

logger = logging.getLogger("launcher")


class EmulatorLauncherBase:
    def launch(self, config: Config) -> Accessible:
        raise NotImplementedError()

    def find_application(self, application_name: str) -> Accessible:
        registry = pyatspi.Registry()
        desktop_count = registry.getDesktopCount()
        for desktop_i in range(desktop_count):
            desktop = registry.getDesktop(desktop_i)
            for app in desktop:
                if app.getRoleName() != "application":
                    continue
                if app.name == application_name:
                    return app
        raise KeyError(application_name)

    def _launch_application(self, app_path: str,
                            main_window_title: str,
                            wait_seconds_after_launch: float = 3,
                            click_after_launch: bool = True,
                            wait_seconds_after_click: float = 1,
                            assert_focused: bool = True) \
            -> Accessible:
        logger.info(f'Launching the application {app_path}.')
        application = None
        command = app_path.split(" ")
        try:
            application = Popen(command)
            error = None
        except Exception as e:
            error = e
        if error is not None:
            logger.error(f"Error has occurred while launching application: {error}.")
            logger.error(f"Terminating...")
            if application is not None:
                application.kill()
            raise ValueError(f'Failed to launch the application {app_path} cause of {str(error)}.')
        logger.info(f"Waiting for application wake up in {wait_seconds_after_launch} seconds.")
        time.sleep(wait_seconds_after_launch)

        application_name, main_window_name = main_window_title.split(".", maxsplit=1)

        logger.info(f"Looking for an application by name {application_name}")
        application = self.find_application(application_name)

        logger.info(f"Looking for application main window {main_window_name}.")
        main_window = find_window_by_exact_name(application, main_window_name)

        if click_after_launch:
            logger.info(f"Clicking at the main window center location.")
            x, y = center_of_element(main_window)
            registry = pyatspi.Registry()
            registry.generateMouseEvent(x, y, "b1p")
            time.sleep(wait_seconds_after_click)

        if assert_focused:
            logger.info(f"Making sure that the application's main window is focused.")
            is_active = STATE_ACTIVE in main_window.getState().getStates()
            if not is_active:
                logger.error(f"The application's main window is not focused correctly.")
                logger.error(f"Terminating...")
                raise ValueError(f"Failed at main window focus check.")

        return application
