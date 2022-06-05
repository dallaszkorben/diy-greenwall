import os
import configparser
from pathlib import Path
import logging

from greenwall.config.property import Property
from greenwall.config.ini_location import IniLocation

class Config( Property ):
    INI_FILE_NAME="config.ini"

    # (section, key, default)

    DEFAULT_GENERAL_GADGET_NAME = ("general", "gadget-name", "GreenWall")

    DEFAULT_LOG_LEVEL = ("log", "level", "DEBUG")
    DEFAULT_LOG_FILE_NAME = ("log", "file-name", "greenwall.log")
    DEFAULT_LOG_FOLDER_NAME = ("log", "folder-name", "DEBUG")

    DEFAULT_LOG_REGISTER_LAMP_FILE_NAME = ("log.register", "lamp-file-name", "lamp_register.log")
    DEFAULT_LOG_REGISTER_PUMP_FILE_NAME = ("log.register", "pump-file-name", "pump_register.log")
    DEFAULT_LOG_REGISTER_CAM_FILE_NAME = ("log.register", "cam-file-name", "cam_register.log")

    DEFAULT_SENSOR_REPORT_FILE_NAME = ("sensor-report", "file-name", "sensor_report.log")

    DEFAULT_WEB_ROOT_PATH = ("web", "root-path", "/var/www/greenwall")
    DEFAULT_WEB_CAM_FRAME_FOLDER = ("web", "cam-frame-folder", "cam-frame")
    DEFAULT_WEB_CAM_CAPTURE_FOLDER = ("web", "cam-capture-folder", "cam-capture")
    DEFAULT_WEB_CAM_CAPTURE_FILE = ("web", "cam-capture-file", "capture.jpg")
    DEFAULT_WEB_SMOOTHING_WINDOW = ("web", "smoothing-window", 15)

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

    def getLogRegisterLampFileName(self):
        return self.get(self.DEFAULT_LOG_REGISTER_LAMP_FILE_NAME[0], self.DEFAULT_LOG_REGISTER_LAMP_FILE_NAME[1], self.DEFAULT_LOG_REGISTER_LAMP_FILE_NAME[2])

    def getLogRegisterPumpFileName(self):
        return self.get(self.DEFAULT_LOG_REGISTER_PUMP_FILE_NAME[0], self.DEFAULT_LOG_REGISTER_PUMP_FILE_NAME[1], self.DEFAULT_LOG_REGISTER_PUMP_FILE_NAME[2])

    def getLogRegisterCamFileName(self):
        return self.get(self.DEFAULT_LOG_REGISTER_CAM_FILE_NAME[0], self.DEFAULT_LOG_REGISTER_CAM_FILE_NAME[1], self.DEFAULT_LOG_REGISTER_CAM_FILE_NAME[2])

    def getSensorReportFileName(self):
        return self.get(self.DEFAULT_SENSOR_REPORT_FILE_NAME[0], self.DEFAULT_SENSOR_REPORT_FILE_NAME[1], self.DEFAULT_SENSOR_REPORT_FILE_NAME[2])

    def getWebRootPath(self):
        return self.get(self.DEFAULT_WEB_ROOT_PATH[0], self.DEFAULT_WEB_ROOT_PATH[1], self.DEFAULT_WEB_ROOT_PATH[2])

    def getWebCamFrameFolder(self):
        return self.get(self.DEFAULT_WEB_CAM_FRAME_FOLDER[0], self.DEFAULT_WEB_CAM_FRAME_FOLDER[1], self.DEFAULT_WEB_CAM_FRAME_FOLDER[2])

    def getWebCamCaptureFolder(self):
        return self.get(self.DEFAULT_WEB_CAM_CAPTURE_FOLDER[0], self.DEFAULT_WEB_CAM_CAPTURE_FOLDER[1], self.DEFAULT_WEB_CAM_CAPTURE_FOLDER[2])

    def getWebCamCaptureFile(self):
        return self.get(self.DEFAULT_WEB_CAM_CAPTURE_FILE[0], self.DEFAULT_WEB_CAM_CAPTURE_FILE[1], self.DEFAULT_WEB_CAM_CAPTURE_FILE[2])

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
        self.update(self.DEFAULT_LOG_FILE_NAME[0], self.DEFAULT_LOG_FILE_NAME[1], logFileName)

    def setLogFolderName(self, logFolderName):
        self.update(self.DEFAULT_LOG_FOLDER_NAME[0], self.DEFAULT_LOG_FOLDER_NAME[1], logFolderName)

    def setLogRegisterLampFileName(self, registerFileName):
        self.update(self.DEFAULT_LOG_REGISTER_LAMP_FILE_NAME[0], self.DEFAULT_LOG_REGISTER_LAMP_FILE_NAME[1], registerFileName)

    def setLogRegisterPumpFileName(self, registerFileName):
        self.update(self.DEFAULT_LOG_REGISTER_PUMP_FILE_NAME[0], self.DEFAULT_LOG_REGISTER_PUMP_FILE_NAME[1], registerFileName)

    def setLogRegisterCamFileName(self, registerFileName):
        self.update(self.DEFAULT_LOG_REGISTER_CAM_FILE_NAME[0], self.DEFAULT_LOG_REGISTER_CAM_FILE_NAME[1], registerFileName)

    def setSensorReportFileName(self, reportFileName):
        self.update(self.DEFAULT_SENSOR_REPORT_FILE_NAME[0], self.DEFAULT_SENSOR_REPORT_FILE_NAME[1], reportFileName)

    def setWebRootPath(self, webRootPath):
        self.update(self.DEFAULT_WEB_ROOT_PATH[0], self.DEFAULT_WEB_ROOT_PATH[1], webRoothPath)

    def setWebCamFrameFolder(self, webCamFrameFolder):
        self.update(self.DEFAULT_WEB_CAM_FRAME_FOLDER[0], self.DEFAULT_WEB_CAM_FRAME_FOLDER[1], webCamFrameFolder)

    def setWebCamCaptureFolder(self, webCamCaptureFolder):
        self.update(self.DEFAULT_WEB_CAM_CAPTURE_FOLDER[0], self.DEFAULT_WEB_CAM_CAPTURE_FOLDER[1], webCamCaptureFolder)

    def setWebCamCaptureFile(self, webCamCaptureFile):
        self.update(self.DEFAULT_WEB_CAM_CAPTURE_FILE[0], self.DEFAULT_WEB_CAM_CAPTURE_FILE[1], webCamCaptureFile)

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

    config["log-register-lamp-file-name"] = cb.getLogRegisterLampFileName()
    config["log-register-pump-file-name"] = cb.getLogRegisterPumpFileName()
    config["log-register-cam-file-name"] = cb.getLogRegisterCamFileName()

    config["web-root-path"] = cb.getWebRootPath()
    config["web-cam-frame-folder"] = cb.getWebCamFrameFolder()
    config["web-cam-capture-folder"] = cb.getWebCamCaptureFolder()
    config["web-cam-capture-file"] = cb.getWebCamCaptureFile()
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

    if "log-register-lamp-file-name" in config:
        cb.setLogRegisterLampFileName(config["log-register-lamp-file-name"])

    if "log-register-pump-file-name" in config:
        cb.setLogRegisterPumpFileName(config["log-register-lamp-file-name"])

    if "log-register-cam-file-name" in config:
        cb.setLogRegisterCamFileName(config["log-register-cam-file-name"])

    if "web-root-path" in config:
        cb.setWebRootPath(config["web-root-path"])

    if "web-cam-frame-folder" in config:
        cb.setWebCamFrameFolder(config["web-cam-frame-folder"])

    if "web-cam-capture-folder" in config:
        cb.setWebCamCaptureFolder(config["web-cam-capture-folder"])

    if "web-cam-capture-file" in config:
        cb.setWebCamCaptureFile(config["web-cam-capture-file"])

    if "web-smoothing-window" in config:
        cb.setWebSmoothingWindow(config["web-smoothing-window"])

#    if "pump-id" in config:
#        cb.setPumpId(config["pump-id"])
#
#    if "pump-gpio" in config:
#        cb.setPumpGpio(config["pump-gpio"])

