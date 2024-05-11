import logging
from typing import Any

from dsrobo.config import Config, JobConfig

logger = logging.getLogger('rom_loader')


class RomLoaderBase(object):
    def load_rom(self, application: Any,
                 config: Config, job_config: JobConfig):
        raise NotImplementedError()
