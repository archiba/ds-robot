import logging

from atomacos import NativeUIElement

from dsrobo.config import Config, JobConfig

logger = logging.getLogger('rom_loader')


class RomLoaderBase(object):
    def load_rom(self, application: NativeUIElement,
                 config: Config, job_config: JobConfig):
        raise NotImplementedError()
