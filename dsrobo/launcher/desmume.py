from dsrobo.config import Config
from dsrobo.launcher.base import EmulatorLauncherBase


class DeSmuMELauncher(EmulatorLauncherBase):
    def launch(self, config: Config):
        return self._launch_application(
            config.desmume.application_path,
            config.desmume.main_window_name,
            config.desmume.action.launch__after_launch_wait_seconds,
            config.desmume.action.launch__click_after_launch,
            config.desmume.action.launch__after_click_wait_seconds,
            config.desmume.action.launch__assert_focus_after_launch
        )
