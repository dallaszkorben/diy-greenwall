import logging
from exceptions.invalid_api_usage import InvalidAPIUsage
from webserver.endpoints.ep import EP

class EPInfoRequest(EP):

    NAME = 'info_request'
    URL = '/info/request'

    URL_ROUTE_PAR_PAYLOAD = '/'
    URL_ROUTE_PAR_URL = '/request'

    METHOD = 'GET'

    #ATTR_ACTUATOR_ID = 'actuatorId'

    def __init__(self, web_gadget):
        self.web_gadget = web_gadget

    def getRequestDescriptionWithPayloadParameters(self):

        ret = {}
        ret['name'] = EPInfo.NAME
        ret['url'] = EPInfo.URL_ROUTE_PAR_PAYLOAD
        ret['method'] = EPInfo.METHOD

        ret['payload-desc'] = [{},{}]

        return ret

    def executeByParameters(self, actuatorId) -> dict:
        payload = {}
        return self.executeByPayload(payload)

    def executeByPayload(self, payload) -> dict:

        logging.debug( "WEB request: {0} {1}".format(
            EPInfo.METHOD, EPInfo.URL,
            )
        )

        return self.getRequestDescriptionWithPayloadParameters()