
import logging
from exceptions.invalid_api_usage import InvalidAPIUsage
from wgadget.endpoints.ep import EP

class EPInfoLight(EP):

    NAME = 'info_light'
    URL = '/info'

    URL_ROUTE_PAR_PAYLOAD = '/'
    URL_ROUTE_PAR_URL = '/actuatorId/<actuatorId>'

    METHOD = 'GET'

    ATTR_ACTUATOR_ID = 'actuatorId'

    def __init__(self, web_gadget):
        self.web_gadget = web_gadget

    def getRequestDescriptionWithPayloadParameters(self):

        ret = {}
        ret['name'] = EPInfoLight.NAME
        ret['url'] = EPInfoLight.URL_ROUTE_PAR_PAYLOAD
        ret['method'] = EPInfoLight.METHOD

        ret['payload-desc'] = [{},{}]

        ret['payload-desc'][0]['attribute'] = EPInfoLight.ATTR_ACTUATOR_ID
        ret['payload-desc'][0]['type'] = 'integer'
        ret['payload-desc'][0]['value'] = 1

        return ret

    def executeByParameters(self, actuatorId) -> dict:
        payload = {}
        payload[EPInfoLight.ATTR_ACTUATOR_ID] = int(actuatorId)
        return self.executeByPayload(payload)

    def executeByPayload(self, payload) -> dict:

        actuatorId = int(payload[EPInfoLight.ATTR_ACTUATOR_ID])

        if actuatorId == self.web_gadget.getLightId():

            actualValue = self.web_gadget.fetchSavedLightValue()

            logging.debug( "WEB request: {0} {1} ('{2}': {3})".format(
                EPInfoLight.METHOD, EPInfoLight.URL,
                EPInfoLight.ATTR_ACTUATOR_ID, actuatorId)
            )

            return {"value": actualValue, "thread": self.web_gadget.getThreadControllerStatus()}
#            return {"value": actualValue, "thread": {"inProgress": False, "id":1}}

        else:
            raise InvalidAPIUsage("No such actuator: {0} or value: {1}".format(actuatorId, value), error_code=404)
