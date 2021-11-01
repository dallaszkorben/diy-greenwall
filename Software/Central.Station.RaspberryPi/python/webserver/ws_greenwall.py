import os
import logging
from logging.handlers import RotatingFileHandler

from threading import Lock

from datetime import datetime
import tzlocal
import time

import json
from flask import Flask
from flask import jsonify
from flask import session
from flask_classful import FlaskView, route, request
from flask_cors import CORS

from webserver.view_info import InfoView
from webserver.view_report_level import ReportlevelView
from webserver.gradual_thread_controller import GradualThreadController

from threading import Thread

#from config.permanent_data import getPermanentData
from config.config import getConfig
from config.ini_location import IniLocation

class WSGreenWall(Flask):

    def __init__(self, import_name):

        self.gradualThreadController = GradualThreadController.getInstance()

        self.lock = Lock()

        cg = getConfig()

        self.name = cg["gadget-name"]
        logLevel = cg["log-level"]
        logFileName = cg["log-file-name"]
        self.pumpId = cg["actuator-pump-id"]
        self.pumpPin = cg["actuator-pump-pin"]
        self.sensorTemperatureId = cg["sensor-temperature-id"]
        self.sensorTemperaturePin = cg["sensor-temperature-pin"]
        self.sensorHumidityId = cg["sensor-humidity-id"]
        self.sensorHumidityPin = cg["sensor-humidity-pin"]

        # LOG 
        logFolder = IniLocation.get_path_to_config_folder()
        logPath = os.path.join(logFolder, logFileName)
        logging.basicConfig(
            handlers=[RotatingFileHandler(logPath, maxBytes=5*1024*1024, backupCount=5)],
            format='%(asctime)s %(levelname)8s - %(message)s' , 
            level = logging.ERROR if logLevel == 'ERROR' else logging.WARNING if logLevel == 'WARNING' else logging.INFO if logLevel == 'INFO' else logging.DEBUG if logLevel == 'DEBUG' else 'CRITICAL' )

        # TODO remove self.app and correnct the references
        super(WSGreenWall, self).__init__(import_name)

        self.app = self
        #self.app = Flask(__name__)
        #self.app.logger.setLevel(logging.ERROR)

        # This will enable CORS for all routes
        CORS(self.app)

        # register the end-points
        InfoView.register(self.app, init_argument=self)
        ReportlevelView.register(self.app, init_argument=self)

        #self.process = {"inProgress": False, "processId": None}

    def getThreadControllerStatus(self):
        return self.gradualThreadController.getStatus()

    def unconfigure(self):
        pass
#        self.egLight.unconfigure()

    # Because of WSGI
    def run(self, host=None, port=None, debug=None, load_dotenv=True, **options):
        super(WSGreenWall, self).run(host=host, port=port, debug=debug, load_dotenv=load_dotenv, **options)


    def __del__(self):
#        logging.debug("__del__() method is called")
        self.unconfigure()

# because of WSGI
app = WSGreenWall(__name__)
