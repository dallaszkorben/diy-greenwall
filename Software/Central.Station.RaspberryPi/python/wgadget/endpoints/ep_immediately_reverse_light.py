from exceptions.invalid_api_usage import InvalidAPIUsage
import logging
from wgadget.endpoints.ep import EP

class EPImmediatelyReverseLight(EP):

    NAME = 'reverse_light_immediately'
    URL = '/immediately/reverse'

    URL_ROUTE_PAR_PAYLOAD = '/reverse'
    URL_ROUTE_PAR_URL = '/reverse/actuatorId/<actuatorId>'

    METHOD = 'POST'

    ATTR_ACTUATOR_ID = 'actuatorId'

    def __init__(self, web_gadget):
        self.web_gadget = web_gadget

    def getRequestDescriptionWithPayloadParameters(self):

        ret = {}
        ret['name'] = EPImmediatelyReverseLight.NAME
        ret['url'] = EPImmediatelyReverseLight.URL_ROUTE_PAR_PAYLOAD
        ret['method'] = EPImmediatelyReverseLight.METHOD

        ret['payload-desc'] = [{}]

        ret['payload-desc'][0]['attribute'] = EPImmediatelyReverseLight.ATTR_ACTUATOR_ID
        ret['payload-desc'][0]['type'] = 'integer'
        ret['payload-desc'][0]['value'] = 1

        return ret

    def executeByParameters(self, actuatorId) -> dict:

        payload = {}
        payload[EPImmediatelyReverseLight.ATTR_ACTUATOR_ID] = int(actuatorId)
        return self.executeByPayload(payload)


    def executeByPayload(self, payload) -> dict:

        actuatorId = int(payload[EPImmediatelyReverseLight.ATTR_ACTUATOR_ID])

        if actuatorId == self.web_gadget.getLightId():

            # Stop the running Thread
            self.web_gadget.gradualThreadController.indicateToStop()
            while self.web_gadget.gradualThreadController.isRunning():
                logging.debug( "  Waitiong for thread stops")

            logging.debug( "WEB request: {0} {1} ('{2}': {3})".format(
                EPImmediatelyReverseLight.METHOD, EPImmediatelyReverseLight.URL,
                EPImmediatelyReverseLight.ATTR_ACTUATOR_ID, actuatorId)
            )

            # Save the light value and set the Light
            return self.web_gadget.reverseLight()

        else:
            raise InvalidAPIUsage("No such actuator: {0}".format(actuatorId), status_code=404)
