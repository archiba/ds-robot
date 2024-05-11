import time

import atomacos
from atomacos import NativeUIElement
import logging

from dsrobo.config import Config
from dsrobo.util.mac import center_of_element, find_window_by_exact_name

logger = logging.getLogger("launcher")


class EmulatorLauncherBase:
    def launch(self, config: Config) -> NativeUIElement:
        raise NotImplementedError()

    def _launch_application(self, app_path: str,
                            main_window_title: str,
                            wait_seconds_after_launch: float = 3,
                            click_after_launch: bool = True,
                            wait_seconds_after_click: float = 1,
                            assert_focused: bool = True) \
            -> NativeUIElement:
        logger.info(f'Launching the application {app_path}.')
        application_info, error = atomacos.launchAppByBundlePath(app_path)
        if error is not None:
            logger.error(f"Error has occurred while launching application: {error}.")
            logger.error(f"Terminating...")
            raise ValueError(f'Failed to launch the application {app_path} cause of {str(error)}.')
        logger.info(f"Waiting for application wake up in {wait_seconds_after_launch} seconds.")
        time.sleep(wait_seconds_after_launch)

        logger.info(f"Acquiring application bundle id")
        bundle_id = application_info.bundleIdentifier()
        logger.info(f"Connecting to the application process with bundle id {bundle_id}.")
        application = atomacos.getAppRefByBundleId(bundle_id)

        logger.info(f'Looking for the main window of the application by title {main_window_title}.')
        main_window = find_window_by_exact_name(application, main_window_title)
        if main_window is None:
            logger.error(f"Could not find a main window(title={main_window_title}) of the application.")
            logger.error('Terminating...')
            raise ValueError(f'Failed to find a main window(title={main_window_title}')

        if click_after_launch:
            logger.info(f"Clicking at the main window center location.")
            x, y = center_of_element(main_window)
            atomacos.mouse.click(x=x, y=y)
            time.sleep(wait_seconds_after_click)

        if assert_focused:
            logger.info(f"Making sure that the application's main window is focused.")
            if not getattr(main_window, 'AXFocused', False):
                logger.error(f"The application's main window is not focused correctly.")
                logger.error(f"Terminating...")
                raise ValueError(f"Failed at main window focus check.")

        return application
