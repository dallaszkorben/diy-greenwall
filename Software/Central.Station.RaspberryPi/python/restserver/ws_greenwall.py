import os
import logging

from controlbox.controlbox import Controlbox

from logging.handlers import RotatingFileHandler
from dateutil import parser

from datetime import datetime
import time

import json
from flask import Flask
from flask import jsonify
from flask import session
from flask_classful import FlaskView, route, request
from flask_cors import CORS

from restserver.view_info import InfoView
from restserver.view_level import LevelView

from config.config import getConfig
from config.ini_location import IniLocation

from utilities.report import Report

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

        reportFileName = cg["report-file-name"]

        self.webFolderName = cg["web-folder-name"]
        self.webPathNameGraph = cg["web-path-name-graph"]
        self.webSmoothingWindow = int(cg["web-smoothing-window"])

        # LOG 
        logFolder = IniLocation.get_path_to_config_folder()
        logPath = os.path.join(logFolder, logFileName)
        logging.basicConfig(
            handlers=[RotatingFileHandler(logPath, maxBytes=5*1024*1024, backupCount=5)],
            format='%(asctime)s %(levelname)8s - %(message)s' , 
            level = logging.ERROR if logLevel == 'ERROR' else logging.WARNING if logLevel == 'WARNING' else logging.INFO if logLevel == 'INFO' else logging.DEBUG if logLevel == 'DEBUG' else 'CRITICAL' )

        # REPORT
        reportFolder = IniLocation.get_path_to_config_folder()
        self.reportPath = os.path.join(reportFolder, reportFileName)

        # TODO remove self.app and correnct the references
#        super(WSGreenWall, self).__init__(import_name)
#        super().__init__(import_name)


        # This will enable CORS for all routes
        CORS(self.app)

        self.report = Report(self.reportPath)

        # register the end-points
        InfoView.register(self.app, init_argument=self)
        LevelView.register(self.app, init_argument=self)

        self.controlbox = Controlbox(self.app)

    def getThreadControllerStatus(self):
        return self.gradualThreadController.getStatus()

    def unconfigure(self):
        pass
#        self.egLight.unconfigure()

#    # Because of WSGI
#    def run(self, host=None, port=None, debug=None, load_dotenv=True, use_reloader=False, **options):
#        self.app.run(host=host, port=port, debug=debug, use_reloader=False)
#        super(WSGreenWall, self).run(host=host, port=port, debug=debug, load_dotenv=load_dotenv, **options)

    def __del__(self):
        self.unconfigure()

#
## because of WSGI
#app = WSGreenWall(__name__)
