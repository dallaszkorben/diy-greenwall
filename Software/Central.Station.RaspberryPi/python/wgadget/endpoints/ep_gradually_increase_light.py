
import logging
from threading import Thread
from threading import get_ident
from exceptions.invalid_api_usage import InvalidAPIUsage
from wgadget.endpoints.ep import EP

class EPGraduallyIncreaseLight(EP):

    NAME = 'increase_light_gradually'
    URL = '/gradually/increase'

    URL_ROUTE_PAR_PAYLOAD = '/increase'
    URL_ROUTE_PAR_URL = '/increase/actuatorId/<actuatorId>/stepValue/<stepValue>/inSeconds/<inSeconds>'

    METHOD = 'POST'

    ATTR_ACTUATOR_ID = 'actuatorId'
    ATTR_STEP_VALUE = 'stepValue'
    ATTR_IN_SECONDS = 'inSeconds'

    def __init__(self, web_gadget):
        self.web_gadget = web_gadget

    def getRequestDescriptionWithPayloadParameters(self):

        ret = {}
        ret['name'] = EPGraduallyIncreaseLight.NAME
        ret['url'] = EPGraduallyIncreaseLight.URL_ROUTE_PAR_PAYLOAD
        ret['method'] = EPGraduallyIncreaseLight.METHOD

        ret['payload-desc'] = [{},{},{}]

        ret['payload-desc'][0]['attribute'] = EPGraduallyIncreaseLight.ATTR_ACTUATOR_ID
        ret['payload-desc'][0]['type'] = 'integer'
        ret['payload-desc'][0]['value'] = 1

        ret['payload-desc'][1]['attribute'] = EPGraduallyIncreaseLight.ATTR_STEP_VALUE
        ret['payload-desc'][1]['type'] = 'integer'
        ret['payload-desc'][1]['min'] = -100
        ret['payload-desc'][1]['max'] = 100

        ret['payload-desc'][2]['attribute'] = EPGraduallyIncreaseLight.ATTR_IN_SECONDS
        ret['payload-desc'][2]['type'] = 'integer'
        ret['payload-desc'][2]['min'] = 0
        ret['payload-desc'][2]['max'] = None

        return ret

    def executeByParameters(self, actuatorId, stepValue, inSeconds):
        payload = {}
        payload[EPGraduallyIncreaseLight.ATTR_ACTUATOR_ID] = int(actuatorId)
        payload[EPGraduallyIncreaseLight.ATTR_STEP_VALUE] = int(stepValue)
        payload[EPGraduallyIncreaseLight.ATTR_IN_SECONDS] = int(inSeconds)
        self.executeByPayload(payload)


    def executeByPayload(self, payload):

        actuatorId = int(payload[EPGraduallyIncreaseLight.ATTR_ACTUATOR_ID])
        stepValue = int(payload[EPGraduallyIncreaseLight.ATTR_STEP_VALUE])
        inSeconds = int(payload[EPGraduallyIncreaseLight.ATTR_IN_SECONDS])

        if actuatorId == self.web_gadget.getLightId():

            # Stop the running Thread
            self.web_gadget.gradualThreadController.indicateToStop()
            while self.web_gadget.gradualThreadController.isRunning():
                logging.debug( "  Waitiong for thread stops")

            actualValue = self.web_gadget.fetchSavedLightValue()
            newValue = actualValue['current'] + stepValue
            newValue = min(100, newValue) if stepValue > 0 else max(0, newValue)

            logging.debug( "{0} {1} ('{2}': {3}, '{4}': {5}, '{6}': {7})  fromValue: {8}, toValue: {9}".format(
                        EPGraduallyIncreaseLight.METHOD, EPGraduallyIncreaseLight.URL,
                        EPGraduallyIncreaseLight.ATTR_ACTUATOR_ID, actuatorId,
                        EPGraduallyIncreaseLight.ATTR_STEP_VALUE, stepValue,
                        EPGraduallyIncreaseLight.ATTR_IN_SECONDS, inSeconds,
                        actualValue['current'], newValue)
            )

            #thread = Thread(target = self.web_gadget.setLight, args = (actuatorId, actualValue['current'], newValue, inSeconds)) 
            #thread = Thread(target = self.web_gadget.setLight, args = (newValue, actualValue['current'], inSeconds)) 

            thread = Thread(target = self.runThread, args = (newValue, actualValue['current'], inSeconds)) 

            thread.daemon = True
            thread.start()

        else:
            raise InvalidAPIUsage("No such actuator: {0} or step value: {1} or seconds {2}".format(actuatorId, stepValue, inSeconds), error_code=404)

        return {'status': 'OK'}

    # THREAD
    def runThread(self, newValue, actualValue, inSeconds):

        self.web_gadget.gradualThreadController.run(get_ident())

        self.web_gadget.setLight(newValue, actualValue, inSeconds);

        self.web_gadget.gradualThreadController.stopRunning()
