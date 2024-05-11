import time

import atomacos
from atomacos import NativeUIElement

from dsrobo.config import Config, JobConfig
from dsrobo.rom_loader.base import RomLoaderBase, logger
from dsrobo.util import get_rom_abspath
from dsrobo.util.mac import find_window_by_exact_name, open_file_using_cmd_shift_g


class DeSmuMERomLoader(RomLoaderBase):

    def load_rom(self, application: NativeUIElement,
                 config: Config, job_config: JobConfig):
        rom_path, exists = get_rom_abspath(config.rom_directory, job_config.rom_file_path)
        if not exists:
            logger.error(f"Could not find rom file at {rom_path}.")
            logger.error(f"Terminating...")
            raise ValueError(f"Failed to find rom file at {rom_path}.")
        logger.info(f"Loading DeSmuME ROM from file {rom_path}.")

        main_window = find_window_by_exact_name(application, config.desmume.main_window_name)
        if main_window is None:
            logger.error(f"Could not find application's main window by name '{config.desmume.main_window_name}.")
            logger.error(f"Terminating...")
            raise ValueError(f"Failed to find application's main window by name '{config.desmume.main_window_name}")

        logger.info('Opening ROM file selection dialog.')
        atomacos.keyboard.hotkey('command', 'o')
        time.sleep(config.desmume.action.load_rom__before_cmd_shift_g_wait_seconds)
        status = open_file_using_cmd_shift_g(
            application,
            config.desmume.action.load_rom__open_rom_dialog_name,
            rom_path,
            config.desmume.action.load_rom__after_cmd_shift_g_wait_seconds,
            config.desmume.action.load_rom__after_type_path,
            config.desmume.action.load_rom__after_first_enter_wait_seconds,
            config.desmume.action.load_rom__after_second_enter_wait_seconds)
        if not status:
            logger.error(f"Could not open ROM file vai rom selection dialog properly.")
            logger.error(f"Terminating...")
            raise ValueError(f"Failed to open ROM file via rom selection dialog.")
        return
