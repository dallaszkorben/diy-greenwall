import os
import configparser
from pathlib import Path
import logging

from config.property import Property
from config.ini_location import IniLocation

class Config( Property ):
    INI_FILE_NAME="config.ini"

    # (section, key, default)

    DEFAULT_GENERAL_GADGET_NAME = ("general", "gadget-name", "GreenWall")

    DEFAULT_LOG_LEVEL = ("log", "level", "DEBUG")
    DEFAULT_LOG_FILE_NAME = ("log", "file-name", "greenwall.log")
    DEFAULT_LOG_FOLDER_NAME = ("log", "folder-name", "DEBUG")

#    DEFAULT_REPORT_TEMPERATURE_FILE_NAME = ("report", "temperature-file-name", "report-temperature.log")
#    DEFAULT_REPORT_LEVEL_FILE_NAME = ("report", "level-file-name", "report-level.log")
    DEFAULT_REPORT_FILE_NAME = ("report", "file-name", "report-level.log")

    DEFAULT_WEB_FOLDER_NAME = ("web", "folder-name", "/var/www/greenwall")

    DEFAULT_ACTUATOR_PUMP_ID = ("actuator-pump", "id", 1)
    DEFAULT_ACTUATOR_PUMP_PIN = ("actuator-pump", "pin", 18)

#    DEFAULT_SENSOR_TEMPERATURE_ID = ("sensor-temperature", "id", 1)
#    DEFAULT_SENSOR_TEMPERATURE_PIN = ("sensor-temperature", "pin", 17)

#    DEFAULT_SENSOR_HUMIDITY_ID = ("sensor-humidity", "id", 1)
#    DEFAULT_SENSOR_HUMIDITY_PIN = ("sensor-humidity", "pin", 17)

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
        folder = IniLocation.get_path_to_config_folder()
        file = os.path.join(folder, Config.INI_FILE_NAME)
        super().__init__( file, True, folder )

    def getGadgetName(self):
        return self.get(self.DEFAULT_GENERAL_GADGET_NAME[0], self.DEFAULT_GENERAL_GADGET_NAME[1], self.DEFAULT_GENERAL_GADGET_NAME[2])

    def getLogLevel(self):
        return self.get(self.DEFAULT_LOG_LEVEL[0], self.DEFAULT_LOG_LEVEL[1], self.DEFAULT_LOG_LEVEL[2])

    def getLogFileName(self):
        return self.get(self.DEFAULT_LOG_FILE_NAME[0], self.DEFAULT_LOG_FILE_NAME[1], self.DEFAULT_LOG_FILE_NAME[2])

    def getLogFolderName(self):
        return self.get(self.DEFAULT_LOG_FOLDER_NAME[0], self.DEFAULT_LOG_FOLDER_NAME[1], self.DEFAULT_LOG_FOLDER_NAME[2])

#    def getReportTemperatureFileName(self):
#        return self.get(self.DEFAULT_REPORT_TEMPERATURE_FILE_NAME[0], self.DEFAULT_REPORT_TEMPERATURE_FILE_NAME[1], self.DEFAULT_REPORT_TEMPERATURE_FILE_NAME[2])
#    def getReportLevelFileName(self):
#        return self.get(self.DEFAULT_REPORT_LEVEL_FILE_NAME[0], self.DEFAULT_REPORT_LEVEL_FILE_NAME[1], self.DEFAULT_REPORT_LEVEL_FILE_NAME[2])

    def getReportFileName(self):
        return self.get(self.DEFAULT_REPORT_FILE_NAME[0], self.DEFAULT_REPORT_FILE_NAME[1], self.DEFAULT_REPORT_FILE_NAME[2])

    def getWebFolderName(self):
        return self.get(self.DEFAULT_WEB_FOLDER_NAME[0], self.DEFAULT_WEB_FOLDER_NAME[1], self.DEFAULT_WEB_FOLDER_NAME[2])

    def getActuatorPumpId(self):
        return int(self.get(self.DEFAULT_ACTUATOR_PUMP_ID[0], self.DEFAULT_ACTUATOR_PUMP_ID[1], self.DEFAULT_ACTUATOR_PUMP_ID[2]))

    def getActuatorPumpPin(self):
        return int(self.get(self.DEFAULT_ACTUATOR_PUMP_PIN[0], self.DEFAULT_ACTUATOR_PUMP_PIN[1], self.DEFAULT_ACTUATOR_PUMP_PIN[2]))

#    def getSensorTemperatureId(self):
#        return int(self.get(self.DEFAULT_SENSOR_TEMPERATURE_ID[0], self.DEFAULT_SENSOR_TEMPERATURE_ID[1], self.DEFAULT_SENSOR_TEMPERATURE_ID[2]))
#
#    def getSensorTemperaturePin(self):
#        return int(self.get(self.DEFAULT_SENSOR_TEMPERATURE_PIN[0], self.DEFAULT_SENSOR_TEMPERATURE_PIN[1], self.DEFAULT_SENSOR_TEMPERATURE_PIN[2]))
#
#    def getSensorHumidityId(self):
#        return int(self.get(self.DEFAULT_SENSOR_HUMIDITY_ID[0], self.DEFAULT_SENSOR_HUMIDITY_ID[1], self.DEFAULT_SENSOR_HUMIDITY_ID[2]))
#
#    def getSensorHumidityPin(self):
#        return int(self.get(self.DEFAULT_SENSOR_HUMIDITY_PIN[0], self.DEFAULT_SENSOR_HUMIDITY_PIN[1], self.DEFAULT_SENSOR_HUMIDITY_PIN[2]))

# ---

    def setGadgetName(self, gadgetName):
        self.update(self.DEFAULT_GENERAL_GADGET_NAME[0], self.DEFAULT_GENERAL_GADGET_NAME[1], gadgetName)

    def setLogLevel(self, logLevel):
        self.updatet(self.DEFAULT_LOG_LEVEL[0], self.DEFAULT_LOG_LEVEL[1], logLevel)

    def setLogFileName(self, logFileName):
        self.update(self.DEFAULT_LOG_LEVEL[0], self.DEFAULT_LOG_LEVEL[1], logFileName)

    def setLogFolderName(self, logFolderName):
        self.update(self.DEFAULT_LOG_FILE_NAME[0], self.DEFAULT_LOG_FILE_NAME[1], logFolderName)

#    def setReportTemperatureFileName(self, reportFileName):
#        self.update(self.DEFAULT_REPORT_TEMPERATURE_FILE_NAME[0], self.DEFAULT_REPORT_TEMPERATURE_FILE_NAME[1], reportFileName)
#    def setReportLevelFileName(self, reportFileName):
#        self.update(self.DEFAULT_REPORT_LEVEL_FILE_NAME[0], self.DEFAULT_REPORT_LEVEL_FILE_NAME[1], reportFileName)

    def setReportFileName(self, reportFileName):
        self.update(self.DEFAULT_REPORT_FILE_NAME[0], self.DEFAULT_REPORT_FILE_NAME[1], reportFileName)

    def setWebFolderName(self, webFolderName):
        self.update(self.DEFAULT_WEB_FOLDER_NAME[0], self.DEFAULT_WEB_FOLDER_NAME[1], webFolderName)

    def setActuatorPumpId(self, actuatorId):
        self.update(self.DEFAULT_ACTUATOR_PUMP_ID[0], self.DEFAULT_ACTUATOR_PUMP_ID[1], actuatorId)

    def setActuatorPumpPin(self, pwmPin):
        self.update(self.DEFAULT_ACTUATOR_PUMP_PIN[0], self.DEFAULT_ACTUATOR_PUMP_PIN[1], pwmPin)

#    def setSensorTemperatureId(self, sensorId):
#        self.update(self.DEFAULT_SENSOR_TEMPERATURE_ID[0], self.DEFAULT_SENSOR_TEMPERATURE_ID[1], sensorId)
#
#    def setSensorTemperaturePin(self, sensorPin):
#        self.update(self.DEFAULT_SENSOR_TEMPERATURE_PIN[0], self.DEFAULT_SENSOR_TEMPERATURE_PIN[1], sensorPin)
#
#    def setSensorHumidityId(self, sensorId):
#        self.update(self.DEFAULT_SENSOR_HUMIDITY_ID[0], self.DEFAULT_SENSOR_HUMIDITY_ID[1], sensorId)
#
#    def setSensorHumidityPin(self, sensorPin):
#        self.update(self.DEFAULT_SENSOR_HUMIDITY_PIN[0], self.DEFAULT_SENSOR_HUMIDITY_PIN[1], sensorPin)

# ---
# ---

def getConfig():
    cb = Config.getInstance()
    config = {}

    config["gadget-name"] = cb.getGadgetName()

    config["log-level"] = cb.getLogLevel()
    config["log-file-name"] = cb.getLogFileName()
    config["log-folder-name"] = cb.getLogFolderName()

#    config["report-temperature-file-name"] = cb.getReportTemperatureFileName()
#    config["report-level-file-name"] = cb.getReportLevelFileName()

    config["report-file-name"] = cb.getReportFileName()

    config["web-folder-name"] = cb.getWebFolderName()

    config["actuator-pump-id"] = cb.getActuatorPumpId()
    config["actuator-pump-pin"] = cb.getActuatorPumpPin()

#    config["sensor-temperature-id"] = cb.getSensorTemperatureId()
#    config["sensor-temperature-pin"] = cb.getSensorTemperaturePin()
#
#    config["sensor-humidity-id"] = cb.getSensorHumidityId()
#    config["sensor-humidity-pin"] = cb.getSensorHumidityPin()

    return config

def setConfig(config):
    cb = Config.getInstance()

    if "gadget-name" in config:
        cb.setGadgetName(config["gatget-name"])

    if "log-level" in config:
        cb.setLogLevel(config["log-level"])

    if "log-file-name" in config:
        cb.setLogFileName(config["log-file-name"])

    if "log-folder-name" in config:
        cb.setLogFolderName(config["log-folder-name"])

#    if "report-temperature-file-name" in config:
#        cb.setReportTemperatureFileName(config["report-temperature-file-name"])
#    if "report-level-file-name" in config:
#        cb.setReportLevelFileName(config["report-level-file-name"])

    if "report-file-name" in config:
        cb.setReportFileName(config["report-file-name"])

    if "web-folder-name" in config:
        cb.setWebFolderName(config["web-folder-name"])

    if "actuator-pump-id" in config:
        cb.setActuatorPumpId(config["actuator-pump-id"])

    if "actuator-pump-pin" in config:
        cb.setActuatorPumpPin(config["actuator-pump-pin"])

#    if "sensor-Temperature-id" in config:
#         cb.setSensorTemperatureId(config["sensor-temperature-id"])
#
#    if "sensor-Temperature-pin" in config:
#         cb.setSensorTemperaturePin(config["sensor-temperature-pin"])
#
#    if "sensor-Humidity-id" in config:
#         cb.setSensorHumidityId(config["sensor-Humidity-id"])
#
#    if "sensor-Humidity-pin" in config:
#         cb.setSensorHumidityPin(config["sensor-Humidity-pin"])
