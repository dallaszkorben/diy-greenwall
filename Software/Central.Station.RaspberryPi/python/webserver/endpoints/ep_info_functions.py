import logging
from exceptions.invalid_api_usage import InvalidAPIUsage
from webserver.endpoints.ep import EP
from webserver.endpoints.ep_level_add import EPLevelAdd
from webserver.representations import output_json

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

        a1 = EPLevelAdd.getRequestDescriptionWithPayloadParameters()
        a2 = self.getRequestDescriptionWithPayloadParameters()

        data = {}
        resultList = []
        resultList.append(a1)
        resultList.append(a2)
        data["functions"] = resultList
        return output_json(data, EP.CODE_OK)
