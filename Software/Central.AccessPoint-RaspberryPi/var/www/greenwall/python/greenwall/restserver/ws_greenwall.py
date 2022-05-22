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

from greenwall.restserver.view_info import InfoView
from greenwall.restserver.view_sensor import SensorView
from greenwall.restserver.view_cam import CamView
from greenwall.restserver.view_lamp import LampView
from greenwall.restserver.view_pump import PumpView


from greenwall.utilities.report_sensor import ReportSensor
from greenwall.utilities.register_lamp import RegisterLamp
from greenwall.utilities.register_pump import RegisterPump
from greenwall.utilities.register_cam_stream import RegisterCamStream





class WSGreenWall(Flask):
#class WSGreenWall():

    def __init__(self, import_name):

        super().__init__(import_name)

#        self.app = Flask(__name__)
        self.app = self

        cg = getConfig()

        self.name = cg["gadget-name"]
        logLevel = cg["log-level"]
        logFileName = cg["log-file-name"]

        sensorReportFileName = cg["sensor-report-file-name"]
        lampRegisterFileName = cg["lamp-register-file-name"]
        pumpRegisterFileName = cg["pump-register-file-name"]
        camStreamRegisterFileName = cg["cam-stream-register-file-name"]

        self.webFolderName = cg["web-folder-name"]
        self.webPathNameGraph = cg["web-path-name-graph"]
        self.webPathNameCam = cg["web-path-name-cam"]
        self.webSmoothingWindow = int(cg["web-smoothing-window"])

#        self.pumpGpio = cg["pump-gpio"]
#        self.pumpId = cg["pump-id"]

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
        self.lampRegisterPath = os.path.join(reportFolder, lampRegisterFileName)
        self.pumpRegisterPath = os.path.join(reportFolder, pumpRegisterFileName)
        self.camStreamRegisterPath = os.path.join(reportFolder, camStreamRegisterFileName)




















        # This will enable CORS for all routes
        CORS(self.app)

        self.reportSensor = ReportSensor(self.reportPath)
        self.registerLamp = RegisterLamp(self.lampRegisterPath)
        self.registerPump = RegisterPump(self.pumpRegisterPath)
        self.registerCamStream = RegisterCamStream(self.camStreamRegisterPath)

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
