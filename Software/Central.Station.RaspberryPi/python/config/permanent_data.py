import os
import configparser
from pathlib import Path
import logging

from threading import Lock

#from builtins import UnicodeDecodeError

from config.property import Property
from config.ini_location import IniLocation

class PermanentData( Property ):
    INI_FILE_NAME="permanent_data.ini"

    # (section, key, default)
    DEFAULT_ACTUATOR_LIGHT_CURRENT_VALUE = ("actuator", "light-current-value", "0")
    DEFAULT_ACTUATOR_LIGHT_BEFORE_OFF_VALUE = ("actuator", "light-before-off-value", "10")

    __instance = None

    def __new__(cls):
        if cls.__instance == None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    @classmethod
    def getInstance(cls):
        inst = cls.__new__(cls)
        cls.__init__(cls.__instance)
        return inst

# ---

    def __init__(self):
        folder = os.path.join(ConfigLocation.HOME, ConfigLocation.CONFIG_FOLDER)
        file = os.path.join(folder, ConfigExchange.INI_FILE_NAME)
        super().__init__( file, True, folder )

    def getLightCurrentValue(self):
        return self.get(self.DEFAULT_ACTUATOR_LIGHT_CURRENT_VALUE[0], self.DEFAULT_ACTUATOR_LIGHT_CURRENT_VALUE[1], self.DEFAULT_ACTUATOR_LIGHT_CURRENT_VALUE[2])

    def getLightBeforeOffValue(self):
        return self.get(self.DEFAULT_ACTUATOR_LIGHT_BEFORE_OFF_VALUE[0], self.DEFAULT_ACTUATOR_LIGHT_BEFORE_OFF_VALUE[1], self.DEFAULT_ACTUATOR_LIGHT_BEFORE_OFF_VALUE[2])

# ---

    def setLightCurrentValue(self, lightValue):
        self.update(self.DEFAULT_ACTUATOR_LIGHT_CURRENT_VALUE[0], self.DEFAULT_ACTUATOR_LIGHT_CURRENT_VALUE[1], lightValue)

    def setLightBeforeOffValue(self, lightValue):
        self.update(self.DEFAULT_ACTUATOR_LIGHT_BEFORE_OFF_VALUE[0], self.DEFAULT_ACTUATOR_LIGHT_BEFORE_OFF_VALUE[1], lightValue)

# ---
# ---

configLock = Lock()
def getPermanentData():
    with configLock:
        ce = PermanentData.getInstance()
        config = {}

        config['light-current-value'] = ce.getLightCurrentValue()
        config['light-before-off-value'] = ce.getLightBeforeOffValue()

        return config

def setPermanentData(config):
    with configLock:
        ce = PermanentData.getInstance()

        if "light-current-value" in config:
            ce.setLightCurrentValue(config["light-current-value"])

        if "light-before-off-value" in config:
            ce.setLightBeforeOffValue(config["light-before-off-value"])
