import os
import logging
from logging.handlers import RotatingFileHandler



#logPath = "/home/pi/.greenwall/greenwall.log"
#logging.basicConfig(#
#            handlers=[RotatingFileHandler(logPath, maxBytes=5*1024*1024, backupCount=5)],
#            format='%(asctime)s %(levelname)8s - %(message)s' , 
#            level = logging.ERROR )
#logging.error("============= hello =================")
#import getpass
##logging.error( "Env thinks the user is: ");
##logging.error( os.getlogin());
#logging.error( "Effective user is: ");
#logging.error( getpass.getuser());
#
#import pkg_resources
#installed_packages = pkg_resources.working_set
#installed_packages_list = sorted(["%s==%s" % (i.key, i.version) for i in installed_packages])
#logging.error(installed_packages_list)
#logging.error("=====================================")
#print("====== hello ========")
#print("====== Bello ========")




from dateutil import parser

from datetime import datetime
import time

import json
from flask import Flask
from flask import jsonify
from flask import session
from flask_classful import FlaskView, route, request
from flask_cors import CORS

from greenwall.config.config import getConfig
from greenwall.config.ini_location import IniLocation

from greenwall.controlbox.controlbox import Controlbox
from greenwall.lamp.lamp import Lamp
from greenwall.pump.pump import Pump
from greenwall.cam.cam import Cam

from greenwall.restserver.view_info import InfoView
from greenwall.restserver.view_sensor import SensorView
from greenwall.restserver.view_cam import CamView
from greenwall.restserver.view_lamp import LampView
from greenwall.restserver.view_pump import PumpView

from greenwall.utilities.report_sensor import ReportSensor
from greenwall.utilities.register_lamp import RegisterLamp
from greenwall.utilities.register_pump import RegisterPump
from greenwall.utilities.register_cam import RegisterCam

class WSGreenWall(Flask):

    def __init__(self, import_name):

        super().__init__(import_name)

        self.app = self

        cg = getConfig()

        self.name = cg["gadget-name"]
        logLevel = cg["log-level"]
        logFileName = cg["log-file-name"]

        lampRegisterFileName = cg["log-register-lamp-file-name"]
        pumpRegisterFileName = cg["log-register-pump-file-name"]
        camRegisterFileName = cg["log-register-cam-file-name"]

        sensorReportFileName = cg["sensor-report-file-name"]

        self.webRootPath = cg["web-root-path"]
        self.webCamFrameFolder = cg["web-cam-frame-folder"]
        self.webCamVideoFolder = cg["web-cam-video-folder"]
        self.webCamCaptureFolder = cg["web-cam-capture-folder"]
        self.webCamCaptureFile = cg["web-cam-capture-file"]
        self.webSmoothingWindow = int(cg["web-smoothing-window"])

        self.absoluteRootPath = cg["absolute-root-path"]
        self.absoluteCamFrameFolder = cg["absolute-cam-frame-folder"]
        self.absoluteCamVideoFolder = cg["absolute-cam-video-folder"]

        self.timingCamLateRegisterTimeLimit = cg["timing-cam-late-register-time-seconds"]

        # LOG 
        logFolder = IniLocation.get_path_to_config_folder()
        logPath = os.path.join(logFolder, logFileName)
        logging.basicConfig(
            handlers=[RotatingFileHandler(logPath, maxBytes=5*1024*1024, backupCount=5)],
            format='%(asctime)s %(levelname)8s - %(message)s' , 
            level = logging.ERROR if logLevel == 'ERROR' else logging.WARNING if logLevel == 'WARNING' else logging.INFO if logLevel == 'INFO' else logging.DEBUG if logLevel == 'DEBUG' else 'CRITICAL' )

        # REPORT
        reportFolder = IniLocation.get_path_to_config_folder()
        self.reportPath = os.path.join(reportFolder, sensorReportFileName)

        # REGISTER
        registerFolder = IniLocation.get_path_to_config_folder()
        self.lampRegisterPath = os.path.join(registerFolder, lampRegisterFileName)
        self.pumpRegisterPath = os.path.join(registerFolder, pumpRegisterFileName)
        self.camRegisterPath = os.path.join(registerFolder, camRegisterFileName)

        # This will enable CORS for all routes
        CORS(self.app)


# ---

#        import cv2
##        import os
#        from natsort import natsorted
#        start = "5-2022-06-18T17:20"
#        end = "5-2022-06-18T17:50"
#        out=cv2.VideoWriter("/var/www/greenwall/cam-video/video.ogg", cv2.VideoWriter.fourcc(*'theo'), 10, (1024,768))
#        try:
#            print("!!! Start to collect files")
#            for filename in natsorted(os.listdir('/var/www/greenwall/cam-frame')):
#                ext = os.path.splitext(filename)[-1].lower()
#                if ext=='.jpg' and start <= filename <= end:
#                    print(filename)
#                    img=cv2.imread('/var/www/greenwall/cam-frame/' + filename)
#                    out.write(img)
#
#        finally:
#            out.release()
#
#        print("!!! DONE")


# ---

        self.reportSensor = ReportSensor(self.reportPath)

        self.registerLamp = RegisterLamp(self.lampRegisterPath)
        self.registerPump = RegisterPump(self.pumpRegisterPath)
        self.registerCam = RegisterCam(self.app, self.camRegisterPath)

        # register the end-points
        InfoView.register(self.app, init_argument=self)
        SensorView.register(self.app, init_argument=self)
        CamView.register(self.app, init_argument=self)
        LampView.register(self.app, init_argument=self)
        PumpView.register(self.app, init_argument=self)

        self.controlBox = Controlbox(self.app)

        # LAMP
        self.lamp = Lamp(self.app)

        # PUMP
        self.pump = Pump(self.app)

        # CAM
        self.cam = Cam(self.app)

    def getThreadControllerStatus(self):
        return self.gradualThreadController.getStatus()

    def unconfigure(self):
        pass
#        self.egLight.unconfigure()

    def __del__(self):
        self.unconfigure()

print("The FQDN of the main file: %s" % (__name__))

# because of WSGI
app = WSGreenWall(__name__)
