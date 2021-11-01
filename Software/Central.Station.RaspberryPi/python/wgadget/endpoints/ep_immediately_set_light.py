
import logging
from exceptions.invalid_api_usage import InvalidAPIUsage
from wgadget.endpoints.ep import EP

class EPImmediatelySetLight(EP):

    NAME = 'set_light_immediately'
    URL = '/immediately/set'

    URL_ROUTE_PAR_PAYLOAD = '/set'
    URL_ROUTE_PAR_URL = '/set/actuatorId/<actuatorId>/value/<value>'

    METHOD = 'POST'

    ATTR_ACTUATOR_ID = 'actuatorId'
    ATTR_VALUE = 'value'

    def __init__(self, web_gadget):
        self.web_gadget = web_gadget

    def getRequestDescriptionWithPayloadParameters(self):

        ret = {}
        ret['name'] = EPImmediatelySetLight.NAME
        ret['url'] = EPImmediatelySetLight.URL_ROUTE_PAR_PAYLOAD
        ret['method'] = EPImmediatelySetLight.METHOD

        ret['payload-desc'] = [{},{}]

        ret['payload-desc'][0]['attribute'] = EPImmediatelySetLight.ATTR_ACTUATOR_ID
        ret['payload-desc'][0]['type'] = 'integer'
        ret['payload-desc'][0]['value'] = 1


        ret['payload-desc'][1]['attribute'] = EPImmediatelySetLight.ATTR_VALUE
        ret['payload-desc'][1]['type'] = 'integer'
        ret['payload-desc'][1]['min'] = 0
        ret['payload-desc'][1]['max'] = 100

        return ret

    def executeByParameters(self, actuatorId, value) -> dict:
        payload = {}
        payload[EPImmediatelySetLight.ATTR_ACTUATOR_ID] = int(actuatorId)
        payload[EPImmediatelySetLight.ATTR_VALUE] = int(value)
        return self.executeByPayload(payload)


    def executeByPayload(self, payload) -> dict:

        actuatorId = int(payload[EPImmediatelySetLight.ATTR_ACTUATOR_ID])
        value = int(payload[EPImmediatelySetLight.ATTR_VALUE])

        if actuatorId == self.web_gadget.getLightId():

            if value >= 0 and value <= 100:

                # Stop the running Thread
                self.web_gadget.gradualThreadController.indicateToStop()
                while self.web_gadget.gradualThreadController.isRunning():
                    logging.debug( "  Waitiong for thread stops")

                actualValue = self.web_gadget.fetchSavedLightValue()

                logging.debug( "WEB request: {0} {1} ('{2}': {3}, '{4}': {5})".format(
                    EPImmediatelySetLight.METHOD, EPImmediatelySetLight.URL,
                    EPImmediatelySetLight.ATTR_ACTUATOR_ID, actuatorId,
                    EPImmediatelySetLight.ATTR_VALUE, value)
                )

#                if value == 0 and actualValue['current']:

                    # Save the light value and set the Light
#                    return self.web_gadget.setLight(value, actualValue['current'])

#                else:

                    # Save the light value and set the Light
#                    return self.web_gadget.setLight(value)
                return self.web_gadget.setLight(value, actualValue['current'])

            else:
                raise InvalidAPIUsage("The value is not valid: {0}".format(value), error_code=404)

        else:
            raise InvalidAPIUsage("No such actuator: {0} or value: {1}".format(actuatorId, value), error_code=404)
