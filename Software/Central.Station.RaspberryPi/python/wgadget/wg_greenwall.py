
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

from wgadget.immediately import ImmediatelyView
from wgadget.gradually import GraduallyView
from wgadget.info import InfoView
from wgadget.level_view import LevelView
from wgadget.gradual_thread_controller import GradualThreadController

from threading import Thread

from egadget.eg_light import EGLight

from config.config_exchange import getConfigExchange
from config.config_exchange import setConfigExchange
from config.config_egadget import getConfigEGadget

from senact.sa_pwm import SAPwm
from senact.sa_ky040 import SAKy040

from config.config_location import ConfigLocation

class WGGreenWall(Flask):

    def __init__(self, import_name):

        self.gradualThreadController = GradualThreadController.getInstance()

        self.lock = Lock()

        cg = getConfigEGadget()

        self.gadgetName = cg["gadget-name"]
        logLevel = cg["log-level"]
        logFileName = cg["log-file-name"]
        self.actuator1Id = cg["actuator-1-id"]
        self.actuator1PwmPin = cg["actuator-1-pin"]
        self.actuator1PwmFreq = cg["actuator-1-freq"]
        self.actuator1PwmMinDutyCycle = cg["actuator-1-min-duty-cycle"]
        self.actuator1PwmMaxDutyCycle = cg["actuator-1-max-duty-cycle"]
        self.sensor1Id = cg["sensor-1-id"]
        self.sensor1Min = cg["sensor-1-min"]
        self.sensor1Max = cg["sensor-1-max"]
        self.sensor1Step = cg["sensor-1-step"]
        self.sensor1ClockPin = cg["sensor-1-clock-pin"]
        self.sensor1DataPin = cg["sensor-1-data-pin"]
        self.sensor1SwitchPin = cg["sensor-1-switch-pin"]

        # LOG 
        logFolder = ConfigLocation.get_path_to_config_folder()
        logPath = os.path.join(logFolder, logFileName)
        logging.basicConfig(
            handlers=[RotatingFileHandler(logPath, maxBytes=5*1024*1024, backupCount=5)],
            format='%(asctime)s %(levelname)8s - %(message)s' , 
            level = logging.ERROR if logLevel == 'ERROR' else logging.WARNING if logLevel == 'WARNING' else logging.INFO if logLevel == 'INFO' else logging.DEBUG if logLevel == 'DEBUG' else 'CRITICAL' )

        #saPwm = SAPwm(self.actuator1Id, self.actuator1PwmPin, self.actuator1PwmFreq)
        #saKy040 = SAKy040(self.sensor1Id, self.sensor1ClockPin, self.sensor1DataPin, self.sensor1SwitchPin)
        #self.egLight = EGLight( self.gadgetName, saPwm, saKy040, fetchSavedLightValueMethod=self.fetchSavedLightValue, saveLightValueMethod=self.saveLightValue, shouldItStopMethod=self.gradualThreadController.shouldItStop, switchCallbackMethod=None, rotaryCallbackMethod=None )

        # TODO remove self.app and correnct the references

        super(WGGreenWall, self).__init__(import_name)

        self.app = self
        #self.app = Flask(__name__)
        #self.app.logger.setLevel(logging.ERROR)

        # This will enable CORS for all routes
        CORS(self.app)

        # register the end-points
        #ImmediatelyView.register(self.app, init_argument=self)
        #GraduallyView.register(self.app, init_argument=self)
        InfoView.register(self.app, init_argument=self)
        LevelView.register(self.app, init_argument=self)

        #self.process = {"inProgress": False, "processId": None}

    def getThreadControllerStatus(self):
        return self.gradualThreadController.getStatus()

    def getLightId(self):
        return self.actuator1Id

    def getPotmeterId(self):
        return self.sensor1Id

    def unconfigure(self):
        pass
#        self.egLight.unconfigure()

#    def run(self, host='0.0.0.0', debug=False):
#        self.app.run(host=host, debug=debug)

    # Because of WSGI
    def run(self, host=None, port=None, debug=None, load_dotenv=True, **options):
        super(WGGreenWall, self).run(host=host, port=port, debug=debug, load_dotenv=load_dotenv, **options)


    def __del__(self):
#        logging.debug("__del__() method is called")
        self.unconfigure()

    def reverseLight(self):
        return self.egLight.reverseLight()

#    def setLightGradually(self, toValue, fromValue, inSeconds):
    def setLight(self, toValue, fromValue, inSeconds=0):

        return self.egLight.setLight(toValue, fromValue, inSeconds)

    def setLightScheduledGradually(self, toValue, inSeconds, atDateTime):

        timeZone = tzlocal.get_localzone()
        zoneName = timeZone.zone

        atDateTime=atDateTime.astimezone(timeZone).replace(microsecond=0)

        while True:
            time.sleep(1)
            nowDateTime=datetime.now().astimezone(timeZone).replace(microsecond=0)
            if nowDateTime >= atDateTime:
                break

        fromValue = self.fetchSavedLightValue()
        self.egLight.setLight(toValue, fromValue['current'], inSeconds)

    # =====================================================

    def fetchSavedLightValue(self):
        config_ini = getConfigExchange()

        return {
            'current': int(config_ini["light-current-value"]),
            'previous': int(config_ini["light-before-off-value"])

        }

    # =====================================================

    def saveLightValue(self, value, beforeOffValue):

        with self.lock:
            config_ini = getConfigExchange()
            config_ini["light-current-value"] = value
#            if value:
#                config_ini["light-before-off-value"] = value
#            else:
#                config_ini["light-before-off-value"] = beforeOffValue
            config_ini["light-before-off-value"] = beforeOffValue
            setConfigExchange(config_ini)

    # ====================================================


# because of WSGI
app = WGGreenWall(__name__)
