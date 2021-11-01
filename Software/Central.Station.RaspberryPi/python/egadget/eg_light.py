from time import sleep
import logging

import inspect
from types import FrameType
from typing import cast

from senact.sa_pwm import SAPwm
from senact.sa_ky040 import SAKy040
from egadget.eg import EG

class EGLight(EG):

    def __init__(self, gadgetName, actuatorPwm, sensorKy040, fetchSavedLightValueMethod=None, saveLightValueMethod=None, shouldItStopMethod=None, rotaryCallbackMethod=None, switchCallbackMethod=None):

        self.minLightValue = 0
        self.maxLightValue = 100

        self.gadgetName = gadgetName

        self.actuatorPwm = actuatorPwm
        self.sensorKy040 = sensorKy040

        if rotaryCallbackMethod:
            self.sensorKy040.setRotaryCallbackMethod(rotaryCallbackMethod)
        else:
            self.sensorKy040.setRotaryCallbackMethod(self.rotaryCallbackMethod)

        if switchCallbackMethod:
            self.sensorKy040.setSwitchCallbackMethod(switchCallbackMethod)
        else:
            self.sensorKy040.setSwitchCallbackMethod(self.switchCallbackMethod)

        self.fetchSavedLightValueMethod = fetchSavedLightValueMethod
        self.saveLightValueMethod = saveLightValueMethod
        self.shouldItStopMethod = shouldItStopMethod

        self.actuatorPwm.configure()
        self.sensorKy040.configure()

        self.resetLight()

    def getGadgetName(self):
        return self.gadgetName

    def getSensor(self, sensorId):
        if sensorId == self.sensorKy040.id:
            return self.sensorKy040
        else:
            raise AttributeError(f"sensorId={sensorId} is not a valid ID")

    def getSensorKy040(self):
        return self.sensorKy040

    def getActuator(self, actuatorId):
        if actuatorId == self.actuatorPwm.id:
            return self.actuatorPwm
        else:
            raise AttributeError(f"actuatorId={actuatorId} is not a valid ID")

    def getActuatorPwm(self):
        return self.actuatorPwm

    def getSensorIds(self):
        return (self.sensorKy040.id, )

    def getActuatorIds(self):
        return (self.actuatorPwm.id, )

    def resetLight(self):

        if self.fetchSavedLightValueMethod:
            lightValue = self.fetchSavedLightValueMethod()
            lightValue['previous'] = self.minLightValue
        else:
            self.lightValue = {'current': self.maxLightValue, 'previous': self.minLightValue}
            lightValue = self.lightValue

        logging.info("Reset:          current:{0}, previous:{1}".format(lightValue['current'], lightValue['previous']))

        self.setLight(lightValue['current'], lightValue['previous'])

    def setLight(self, toValue, fromValue=None, inSeconds=0):

        if fromValue == None:
            if self.fetchSavedLightValueMethod:
                fromValue = self.fetchSavedLightValueMethod()['current']
            else:
                fromValue = self.lightValue['current']

        logging.info( "Set Light {0} -> {1} in {2} seconds --- FILE: {3}".format(
            fromValue,
            toValue,
            inSeconds,
            __file__)
        )

        pwmValue = self.actuatorPwm.setPwm(toValue, fromValue, inSeconds, self.saveLightValueMethod, self.shouldItStopMethod)

#        if inSeconds:
#            pwmValue = self.actuatorPwm.setPwmByStepValueGradually(toValue, fromValue, inSeconds, self.saveLightValueMethod)
#        else:
#            pwmValue = self.actuatorPwm.setPwmByValue(toValue)



#        if self.saveLightValueMethod:
#            self.saveLightValueMethod(toValue, fromValue)
#        else:
        if not self.saveLightValueMethod:
            self.lightValue['previous'] = fromValue
            self.lightValue['current'] = toValue

        return {'result': 'OK', 'value': toValue}

    def rotaryLight(self, value) -> dict:

        if self.fetchSavedLightValueMethod:
            lightValue = self.fetchSavedLightValueMethod()
        else:
            lightValue = self.lightValue

        newValue = lightValue['current'] + value

        if newValue > self.maxLightValue:
            newValue = self.maxLightValue
        elif newValue < self.minLightValue:
            newValue = self.minLightValue

        return self.setLight(newValue)

    def reverseLight(self, inSeconds=0) -> dict:
        if self.fetchSavedLightValueMethod:
            lightValue = self.fetchSavedLightValueMethod()
        else:
            lightValue = self.lightValue

        if lightValue['current'] > self.minLightValue:
            fromValue = lightValue['current']
            toValue = self.minLightValue
            turned = "off"

        else:
            fromValue = self.minLightValue

            if lightValue['current'] == lightValue['previous']:
                toValue = self.maxLightValue
            else:
                toValue = lightValue['previous']
            turned = "on"

        result = self.setLight(toValue, fromValue, inSeconds)

        return result

    # ==============================================

    def rotaryCallbackMethod(self, value) -> dict:

        return self.rotaryLight(value)

    def switchCallbackMethod(self) -> dict:

        return self.reverseLight()

    # ================================================
