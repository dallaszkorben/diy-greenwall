import os
import configparser
from pathlib import Path
import logging

class IniLocation:
    HOME = str(Path.home())
    FOLDER = '.greenwall'

    @staticmethod 
    def get_path_to_config_folder():
        return os.path.join(IniLocation.HOME, IniLocation.FOLDER)
