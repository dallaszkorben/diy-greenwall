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

    DEFAULT_SENSOR_REPORT_FILE_NAME = ("sensor-report", "file-name", "sensor_report.log")

    DEFAULT_LAMP_REGISTER_FILE_NAME = ("lamp", "file-name", "lamp_register.log")

    DEFAULT_WEB_FOLDER_NAME = ("web", "folder-name-graph", "/var/www/greenwall")
    DEFAULT_WEB_PATH_NAME_GRAPH = ("web", "path-name-graph", "graph-images")
    DEFAULT_WEB_SMOOTHING_WINDOW = ("web", "smoothing-window", 15)

#    DEFAULT_PUMP_ID = ("pump", "id", 1)
#    DEFAULT_PUMP_GPIO = ("pump", "gpio", 26)

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

    def getSensorReportFileName(self):
        return self.get(self.DEFAULT_SENSOR_REPORT_FILE_NAME[0], self.DEFAULT_SENSOR_REPORT_FILE_NAME[1], self.DEFAULT_SENSOR_REPORT_FILE_NAME[2])

    def getLampRegisterFileName(self):
        return self.get(self.DEFAULT_LAMP_REGISTER_FILE_NAME[0], self.DEFAULT_LAMP_REGISTER_FILE_NAME[1], self.DEFAULT_LAMP_REGISTER_FILE_NAME[2])

    def getWebFolderName(self):
        return self.get(self.DEFAULT_WEB_FOLDER_NAME[0], self.DEFAULT_WEB_FOLDER_NAME[1], self.DEFAULT_WEB_FOLDER_NAME[2])

    def getWebPathNameGraph(self):
        return self.get(self.DEFAULT_WEB_PATH_NAME_GRAPH[0], self.DEFAULT_WEB_PATH_NAME_GRAPH[1], self.DEFAULT_WEB_PATH_NAME_GRAPH[2])

    def getWebSmoothingWindow(self):
        return self.get(self.DEFAULT_WEB_SMOOTHING_WINDOW[0], self.DEFAULT_WEB_SMOOTHING_WINDOW[1], self.DEFAULT_WEB_SMOOTHING_WINDOW[2])

#    def getPumpId(self):
#        return int(self.get(self.DEFAULT_PUMP_ID[0], self.DEFAULT_PUMP_ID[1], self.DEFAULT_PUMP_ID[2]))
#
#    def getPumpGpio(self):
#        return int(self.get(self.DEFAULT_PUMP_GPIO[0], self.DEFAULT_PUMP_GPIO[1], self.DEFAULT_PUMP_GPIO[2]))

# ---

    def setGadgetName(self, gadgetName):
        self.update(self.DEFAULT_GENERAL_GADGET_NAME[0], self.DEFAULT_GENERAL_GADGET_NAME[1], gadgetName)

    def setLogLevel(self, logLevel):
        self.updatet(self.DEFAULT_LOG_LEVEL[0], self.DEFAULT_LOG_LEVEL[1], logLevel)

    def setLogFileName(self, logFileName):
        self.update(self.DEFAULT_LOG_LEVEL[0], self.DEFAULT_LOG_LEVEL[1], logFileName)

    def setLogFolderName(self, logFolderName):
        self.update(self.DEFAULT_LOG_FILE_NAME[0], self.DEFAULT_LOG_FILE_NAME[1], logFolderName)

    def setSensorReportFileName(self, reportFileName):
        self.update(self.DEFAULT_SENSOR_REPORT_FILE_NAME[0], self.DEFAULT_SENSOR_REPORT_FILE_NAME[1], reportFileName)

    def setLampRegisterFileName(self, registerFileName):
        self.update(self.DEFAULT_LAMP_REGISTER_FILE_NAME[0], self.DEFAULT_LAMP_REGISTER_FILE_NAME[1], registerFileName)

    def setWebFolderName(self, webFolderName):
        self.update(self.DEFAULT_WEB_FOLDER_NAME[0], self.DEFAULT_WEB_FOLDER_NAME[1], webFolderName)

    def setWebPathNameGraph(self, webPathNameGraph):
        self.update(self.DEFAULT_WEB_PATH_NAME_GRAPH[0], self.DEFAULT_WEB_PATH_NAME_GRAPH[1], webPathNameGraph)

    def setWebSmoothingWindow(self, webSmoothingWindow):
        self.update(self.DEFAULT_WEB_SMOOTHING_WINDOW[0], self.DEFAULT_WEB_SMOOTHING_WINDOW[1], webSmoothingWindow)

#    def setPumpId(self, actuatorId):
#        self.update(self.DEFAULT_PUMP_ID[0], self.DEFAULT_PUMP_ID[1], actuatorId)
#
#    def setPumpGpio(self, gpio):
#        self.update(self.DEFAULT_PUMP_GPIO[0], self.DEFAULT_PUMP_GPIO[1], gpio)

# ---
# ---

def getConfig():
    cb = Config.getInstance()
    config = {}

    config["gadget-name"] = cb.getGadgetName()

    config["log-level"] = cb.getLogLevel()
    config["log-file-name"] = cb.getLogFileName()
    config["log-folder-name"] = cb.getLogFolderName()

    config["sensor-report-file-name"] = cb.getSensorReportFileName()

    config["lamp-register-file-name"] = cb.getLampRegisterFileName()

    config["web-folder-name"] = cb.getWebFolderName()
    config["web-path-name-graph"] = cb.getWebPathNameGraph()
    config["web-smoothing-window"] = cb.getWebSmoothingWindow()

#    config["pump-id"] = cb.getPumpId()
#    config["pump-gpio"] = cb.getPumpGpio()

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

    if "sensor-report-file-name" in config:
        cb.setSensorReportFileName(config["sensor-report-file-name"])

    if "lamp-register-file-name" in config:
        cb.setLampRegisterFileName(config["lamp-register-file-name"])

    if "web-folder-name" in config:
        cb.setWebFolderName(config["web-folder-name"])

    if "web-path-name-graph" in config:
        cb.setWebPathNameGraph(config["web-path-name-graph"])

    if "web-smoothing-window" in config:
        cb.setWebSmoothingWindow(config["web-smoothing-window"])

#    if "pump-id" in config:
#        cb.setPumpId(config["pump-id"])
#
#    if "pump-gpio" in config:
#        cb.setPumpGpio(config["pump-gpio"])

