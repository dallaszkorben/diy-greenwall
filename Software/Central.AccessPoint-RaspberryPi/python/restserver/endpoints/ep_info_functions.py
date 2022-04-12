import logging
from exceptions.invalid_api_usage import InvalidAPIUsage
from restserver.endpoints.ep import EP
from restserver.endpoints.ep_sensor_add import EPSensorAdd
from restserver.endpoints.ep_info_graph import EPInfoGraph

from restserver.representations import output_json

class EPInfoFunctions(EP):

    ID = 'info_functions'
    URL = '/info/functions'

    PATH_PAR_PAYLOAD = '/functions'
    PATH_PAR_URL = '/functions'

    METHOD = 'GET'

    def __init__(self, web_gadget):
        self.web_gadget = web_gadget

    @staticmethod
    def getRequestDescriptionWithPayloadParameters():

        ret = {}
        ret['id'] = EPInfoFunctions.ID
        ret['method'] = EPInfoFunctions.METHOD
        ret['path-parameter-in-payload'] = EPInfoFunctions.PATH_PAR_PAYLOAD
        ret['path-parameter-in-url'] = EPInfoFunctions.PATH_PAR_URL

        ret['parameters'] = []

        return ret

    def executeByParameters(self) -> dict:
        payload = {}
        return self.executeByPayload(payload)

    def executeByPayload(self, payload) -> dict:

        logging.debug( "WEB request: {0} {1}".format(
            EPInfoFunctions.METHOD, EPInfoFunctions.URL,
            )
        )

        a1 = self.getRequestDescriptionWithPayloadParameters()
        a2 = EPSensorAdd.getRequestDescriptionWithPayloadParameters()
        a3 = EPInfoGraph.getRequestDescriptionWithPayloadParameters()

        data = {}
        resultList = []
        resultList.append(a1)
        resultList.append(a2)
#        resultList.append(a3)
        data["functions"] = resultList
        return output_json(data, EP.CODE_OK)
