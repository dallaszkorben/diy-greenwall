import os
import configparser
from pathlib import Path
import logging

class ConfigLocation:
    HOME = str(Path.home())
    CONFIG_FOLDER = '.greenwall'

    @staticmethod 
    def get_path_to_config_folder():
        return os.path.join(ConfigLocation.HOME, ConfigLocation.CONFIG_FOLDER)
