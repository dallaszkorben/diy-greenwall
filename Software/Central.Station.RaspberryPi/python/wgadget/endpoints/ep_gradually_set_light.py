from threading import Thread
from threading import get_ident

from exceptions.invalid_api_usage import InvalidAPIUsage
import logging
from wgadget.endpoints.ep import EP

class EPGraduallySetLight(EP):

    NAME = 'set_light_gradually'
    URL = '/gradually/set'

    URL_ROUTE_PAR_PAYLOAD = '/set'
    URL_ROUTE_PAR_URL = '/set/actuatorId/<actuatorId>/value/<value>/inSeconds/<inSeconds>'

    METHOD = 'POST'

    ATTR_ACTUATOR_ID = 'actuatorId'
    ATTR_VALUE = 'value'
    ATTR_IN_SECONDS = 'inSeconds'

    def __init__(self, web_gadget):
        self.web_gadget = web_gadget

    def getRequestDescriptionWithPayloadParameters(self):

        ret = {}
        ret['name'] = EPGradualySetLight.NAME
        ret['url'] = EPGraduallySetLight.URL_ROUTE_PAR_PAYLOAD
        ret['method'] = EPGraduallySetLight.METHOD

        ret['payload-desc'] = [{},{},{}]

        ret['payload-desc'][0]['attribute'] = EPGraduallySetLight.ATTR_ACTUATOR_ID
        ret['payload-desc'][0]['type'] = 'integer'
        ret['payload-desc'][0]['value'] = 1

        ret['payload-desc'][1]['attribute'] = EPGraduallySetLight.ATTR_VALUE
        ret['payload-desc'][1]['type'] = 'integer'
        ret['payload-desc'][1]['min'] = 0
        ret['payload-desc'][1]['max'] = 100

        ret['payload-desc'][2]['attribute'] = EPGraduallySetLight.ATTR_IN_SECONDS
        ret['payload-desc'][2]['type'] = 'integer'
        ret['payload-desc'][2]['min'] = 0
        ret['payload-desc'][2]['max'] = None

        return ret

    def executeByParameters(self, actuatorId, value, inSeconds):
        payload = {}
        payload[EPGraduallySetLight.ATTR_ACTUATOR_ID] = int(actuatorId)
        payload[EPGraduallySetLight.ATTR_VALUE] = int(value)
        payload[EPGraduallySetLight.ATTR_IN_SECONDS] = int(inSeconds)
        self.executeByPayload(payload)

    def executeByPayload(self, payload):

        actuatorId = int(payload[EPGraduallySetLight.ATTR_ACTUATOR_ID])
        value = int(payload[EPGraduallySetLight.ATTR_VALUE])
        inSeconds = int(payload[EPGraduallySetLight.ATTR_IN_SECONDS])

        if actuatorId == self.web_gadget.getLightId():

            if value >= 0 and value <= 100:

                # Stop the running Thread
                self.web_gadget.gradualThreadController.indicateToStop()
                while self.web_gadget.gradualThreadController.isRunning():
                    logging.debug( "  Waitiong for thread stops")

                actualValue = self.web_gadget.fetchSavedLightValue()
                newValue = value

                logging.debug( "WEB request: {0} {1} ('{2}': {3}, '{4}': {5}, '{6}': {7})".format(
                    EPGraduallySetLight.METHOD, EPGraduallySetLight.URL,
                    EPGraduallySetLight.ATTR_ACTUATOR_ID, actuatorId,
                    EPGraduallySetLight.ATTR_VALUE, value,
                    EPGraduallySetLight.ATTR_IN_SECONDS, inSeconds)
                )

                # Save the light value and set the Light
#                thread = Thread(target = self.web_gadget.setLight, args = (newValue, actualValue['current'], inSeconds)) 
                thread = Thread(target = self.runThread, args = (newValue, actualValue['current'], inSeconds)) 
                thread.daemon = True
                thread.start()

            else:
                raise InvalidAPIUsage("The value is not valid: {0}".format(value), status_code=404)

        else:
            raise InvalidAPIUsage("No such actuator: {0} or value: {1}".format(actuatorId, value), status_code=404)

        return {'status': 'OK'}

    # THREAD
    def runThread(self, newValue, actualValue, inSeconds):

        self.web_gadget.gradualThreadController.run(get_ident())

        self.web_gadget.setLight(newValue, actualValue, inSeconds);

        self.web_gadget.gradualThreadController.stopRunning()

