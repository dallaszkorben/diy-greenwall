import os
import configparser
from pathlib import Path
import logging

from config.property import Property
from config.config_location import ConfigLocation

class ConfigEGadget( Property ):
    INI_FILE_NAME="config_egadget.ini"

    # (section, key, default)

    DEFAULT_GENERAL_GADGET_NAME = ("general", "gadget-name", "Light")

    DEFAULT_LOG_LEVEL = ("log", "level", "DEBUG")
    DEFAULT_LOG_FILE_NAME = ("log", "file-name", "greenwall.log")
    DEFAULT_LOG_FOLDER_NAME = ("log", "folder-name", "DEBUG")

    DEFAULT_ACTUATOR_1_ID = ("actuator-1", "id", 1)
    DEFAULT_ACTUATOR_1_PWM_PIN = ("actuator-1", "pin", 18)
    DEFAULT_ACTUATOR_1_PWM_FREQ = ("actuator-1", "freq", 800)
    DEFAULT_ACTUATOR_1_PWM_MIN_DUTY_CYCLE = ("actuator-1", "min-duty-cycle", 0)
    DEFAULT_ACTUATOR_1_PWM_MAX_DUTY_CYCLE = ("actuator-1", "max-duty-cycle", 1000000)

    DEFAULT_SENSOR_1_ID = ("sensor-1", "id", 1)
    DEFAULT_SENSOR_1_MIN = ("sensor-1", "min", 0)
    DEFAULT_SENSOR_1_MAX = ("sensor-1", "max", 100)
    DEFAULT_SENSOR_1_STEP = ("sensor-1", "step", 1)
    DEFAULT_SENSOR_1_CLOCK_PIN = ("sensor-1", "clock-pin", 17)
    DEFAULT_SENSOR_1_DATA_PIN = ("sensor-1", "data-pin", 27)
    DEFAULT_SENSOR_1_SWITCH_PIN = ("sensor-1", "swithch-pin", 23)

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
        folder = ConfigLocation.get_path_to_config_folder()
        #folder = os.path.join(ConfigLocation.HOME, ConfigLocation.CONFIG_FOLDER)
        file = os.path.join(folder, ConfigEGadget.INI_FILE_NAME)
        super().__init__( file, True, folder )

    def getGadgetName(self):
        return self.get(self.DEFAULT_GENERAL_GADGET_NAME[0], self.DEFAULT_GENERAL_GADGET_NAME[1], self.DEFAULT_GENERAL_GADGET_NAME[2])

    def getLogLevel(self):
        return self.get(self.DEFAULT_LOG_LEVEL[0], self.DEFAULT_LOG_LEVEL[1], self.DEFAULT_LOG_LEVEL[2])

    def getLogFileName(self):
        return self.get(self.DEFAULT_LOG_FILE_NAME[0], self.DEFAULT_LOG_FILE_NAME[1], self.DEFAULT_LOG_FILE_NAME[2])

    def getLogFolderName(self):
        return self.get(self.DEFAULT_LOG_FOLDER_NAME[0], self.DEFAULT_LOG_FOLDER_NAME[1], self.DEFAULT_LOG_FOLDER_NAME[2])

    def getActuator1Id(self):
        return int(self.get(self.DEFAULT_ACTUATOR_1_ID[0], self.DEFAULT_ACTUATOR_1_ID[1], self.DEFAULT_ACTUATOR_1_ID[2]))

    def getActuator1PwmPin(self):
        return int(self.get(self.DEFAULT_ACTUATOR_1_PWM_PIN[0], self.DEFAULT_ACTUATOR_1_PWM_PIN[1], self.DEFAULT_ACTUATOR_1_PWM_PIN[2]))

    def getActuator1PwmFreq(self):
        return int(self.get(self.DEFAULT_ACTUATOR_1_PWM_FREQ[0], self.DEFAULT_ACTUATOR_1_PWM_FREQ[1], self.DEFAULT_ACTUATOR_1_PWM_FREQ[2]))

    def getActuator1PwmMinDutyCycle(self):
        return int(self.get(self.DEFAULT_ACTUATOR_1_PWM_MIN_DUTY_CYCLE[0], self.DEFAULT_ACTUATOR_1_PWM_MIN_DUTY_CYCLE[1], self.DEFAULT_ACTUATOR_1_PWM_MIN_DUTY_CYCLE[2]))

    def getActuator1PwmMaxDutyCycle(self):
        return int(self.get(self.DEFAULT_ACTUATOR_1_PWM_MAX_DUTY_CYCLE[0], self.DEFAULT_ACTUATOR_1_PWM_MAX_DUTY_CYCLE[1], self.DEFAULT_ACTUATOR_1_PWM_MAX_DUTY_CYCLE[2]))

    def getSensor1Id(self):
        return int(self.get(self.DEFAULT_SENSOR_1_ID[0], self.DEFAULT_SENSOR_1_ID[1], self.DEFAULT_SENSOR_1_ID[2]))

    def getSensor1Min(self):
        return int(self.get(self.DEFAULT_SENSOR_1_MIN[0], self.DEFAULT_SENSOR_1_MIN[1], self.DEFAULT_SENSOR_1_MIN[2]))

    def getSensor1Max(self):
        return int(self.get(self.DEFAULT_SENSOR_1_MAX[0], self.DEFAULT_SENSOR_1_MAX[1], self.DEFAULT_SENSOR_1_MAX[2]))

    def getSensor1Step(self):
        return int(self.get(self.DEFAULT_SENSOR_1_STEP[0], self.DEFAULT_SENSOR_1_STEP[1], self.DEFAULT_SENSOR_1_STEP[2]))

    def getSensor1ClockPin(self):
        return int(self.get(self.DEFAULT_SENSOR_1_CLOCK_PIN[0], self.DEFAULT_SENSOR_1_CLOCK_PIN[1], self.DEFAULT_SENSOR_1_CLOCK_PIN[2]))

    def getSensor1DataPin(self):
        return int(self.get(self.DEFAULT_SENSOR_1_DATA_PIN[0], self.DEFAULT_SENSOR_1_DATA_PIN[1], self.DEFAULT_SENSOR_1_DATA_PIN[2]))

    def getSensor1SwitchPin(self):
        return int(self.get(self.DEFAULT_SENSOR_1_SWITCH_PIN[0], self.DEFAULT_SENSOR_1_SWITCH_PIN[1], self.DEFAULT_SENSOR_1_SWITCH_PIN[2]))

# ---

    def setGadgetName(self, gadgetName):
        self.update(self.DEFAULT_GENERAL_GADGET_NAME[0], self.DEFAULT_GENERAL_GADGET_NAME[1], gadgetName)

    def setLogLevel(self, logLevel):
        self.updatet(self.DEFAULT_LOG_LEVEL[0], self.DEFAULT_LOG_LEVEL[1], logLevel)

    def setLogFileName(self, logFileName):
        self.update(self.DEFAULT_LOG_LEVEL[0], self.DEFAULT_LOG_LEVEL[1], logFileName)

    def setLogFolderName(self, logFolderName):
        self.update(self.DEFAULT_LOG_FILE_NAME[0], self.DEFAULT_LOG_FILE_NAME[1], logFolderName)

    def setActuator1Id(self, actuatorId):
        self.update(self.DEFAULT_ACTUATOR_1_ID[0], self.DEFAULT_ACTUATOR_1_ID[1], actuatorId)

    def setActuator1PwmPin(self, pwmPin):
        self.update(self.DEFAULT_ACTUATOR_1_PWM_PIN[0], self.DEFAULT_ACTUATOR_1_PWM_PIN[1], pwmPin)

    def setActuator1PwmFreq(self, pwmFreq):
        self.update(self.DEFAULT_ACTUATOR_1_PWM_FREQ[0], self.DEFAULT_ACTUATOR_1_PWM_FREQ[1], pwmFreq)

    def setActuator1PwmMinDutyCycle(self, pwmMinDutyCycle ):
        self.update(self.DEFAULT_ACTUATOR_1_PWM_MIN_DUTY_CYCLE[0], self.DEFAULT_ACTUATOR_1_PWM_MIN_DUTY_CYCLE[1], pwmMinDutyCycle)

    def setActuator1PwmMaxDutyCycle(self, pwmMaxDutyCycle):
        self.update(self.DEFAULT_ACTUATOR_1_PWM_MAX_DUTY_CYCLE[0], self.DEFAULT_ACTUATOR_1_PWM_MAX_DUTY_CYCLE[1], pwmMaxDutyCycle)

    def setSensor1Id(self, sensorId):
        self.update(self.DEFAULT_SENSOR_1_ID[0], self.DEFAULT_SENSOR_1_ID[1], sensorId)

    def setSensor1Min(self, minValue):
        self.update(self.DEFAULT_SENSOR_1_MIN[0], self.DEFAULT_SENSOR_1_MIN[1], minValue)

    def setSensor1Max(self, maxValue):
        self.update(self.DEFAULT_SENSOR_1_MAX[0], self.DEFAULT_SENSOR_1_MAX[1], maxValue)

    def setSensor1Step(self, valueStep):
        self.update(self.DEFAULT_POTMETER_STEP[0], self.EFAULT_POTMETER_STEP[1], valueStep)

    def setSensor1ClockPin(self, clockPin):
        self.update(self.DEFAULT_SENSOR_1_CLOCK_PIN[0], self.DEFAULT_SENSOR_1_CLOCK_PIN[1], clockPin)

    def setSensor1DataPin(self, dataPin):
        self.update(self.DEFAULT_SENSOR_1_DATA_PIN[0], self.DEFAULT_SENSOR_1_DATA_PIN[1], dataPin)

    def setSensor1SwitchPin(self, switchPin):
        self.update(self.DEFAULT_SENSOR_1_SWITCH_PIN[0], self.DEFAULT_SENSOR_1_SWITCH_PIN[1], switchPin)

# ---
# ---

def getConfigEGadget():
    cb = ConfigEGadget.getInstance()
    config = {}

    config["gadget-name"] = cb.getGadgetName()

    config["log-level"] = cb.getLogLevel()
    config["log-file-name"] = cb.getLogFileName()
    config["log-folder-name"] = cb.getLogFolderName()

    config["actuator-1-id"] = cb.getActuator1Id()
    config["actuator-1-pin"] = cb.getActuator1PwmPin()
    config["actuator-1-freq"] = cb.getActuator1PwmFreq()
    config["actuator-1-min-duty-cycle"] = cb.getActuator1PwmMinDutyCycle()
    config["actuator-1-max-duty-cycle"] = cb.getActuator1PwmMaxDutyCycle()

    config["sensor-1-id"] = cb.getSensor1Id()
    config["sensor-1-min"] = cb.getSensor1Min()
    config["sensor-1-max"] = cb.getSensor1Max()
    config["sensor-1-step"] = cb.getSensor1Step()
    config["sensor-1-clock-pin"] = cb.getSensor1ClockPin()
    config["sensor-1-data-pin"] = cb.getSensor1DataPin()
    config["sensor-1-switch-pin"] = cb.getSensor1SwitchPin()

    return config

def setConfigEGadget(config):
    cb = ConfigEGadget.getInstance()

    if "gadget-name" in config:
        cb.setActuatorGadgetName(config["gadget-name"])

    if "log-level" in config:
        cb.setLogLevel(config["log-level"])

    if "log-file-name" in config:
        cb.setLogFileName(config["log-file-name"])

    if "log-folder-name" in config:
        cb.setLogFolderName(config["log-folder-name"])

    if "actuator-1-id" in config:
        cb.setActuator1Id(config["actuator-1-id"])

    if "actuator-1-pin" in config:
        cb.setActuator1PwmPin(config["actuator-1-pin"])

    if "actuator-1-freq" in config:
        cb.setActuator1PwmFreq(config["actuator-1-freq"])

    if "actuator-1-min-duty-cycle" in config:
        cb.setActuator1PwmMinDutyCycle(config["actuator-1-min-duty-cycle"])

    if "actuator-1-max-duty-cycle" in config:
         cb.setActuator1PwmMaxDutyCycle(config["actuator-1-max-duty-cycle"])

    if "sensor-1-id" in config:
         cb.setSensor1Id(config["sensor-1-id"])

    if "sensor-1-min" in config:
         cb.setSensor1Min(config["sensor-1-min"])

    if "sensor-1-max" in config:
         cb.setSensor1Max(config["sensor-1-max"])

    if "sensor-1-step" in config:
         cb.setSensor1Step(config["sensor-1-step"])

    if "sensor-1-clock-pin" in config:
         cb.setSensor1ClockPin(config["sensor-1-clock-pin"])

    if "sensor-1-data-pin" in config:
         cb.setSensor1DataPin(config["sensor-1-data-pin"])

    if "sensor-1-switch-pin" in config:
         cb.setSensor1SwitchPin(config["sensor-1-switch-pin"])
