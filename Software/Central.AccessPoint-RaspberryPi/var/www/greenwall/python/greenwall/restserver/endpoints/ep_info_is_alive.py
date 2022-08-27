import logging

from greenwall.exceptions.invalid_api_usage import InvalidAPIUsage
from greenwall.restserver.endpoints.ep import EP
from greenwall.restserver.representations import output_json

from flask import request

class EPInfoIsAlive(EP):

    ID = 'info_is_alive'
    URL = '/info/isAlive'

    PATH_PAR_PAYLOAD = '/isAlive'
    PATH_PAR_URL = '/isAlive'

    METHOD = 'GET'

    def __init__(self, web_gadget):
        self.web_gadget = web_gadget

    @staticmethod
    def getRequestDescriptionWithPayloadParameters():

        ret = {}
        ret['id'] = EPInfoIsAlive.ID
        ret['method'] = EPInfoIsAlive.METHOD
        ret['path-parameter-in-payload'] = EPInfoIsAlive.PATH_PAR_PAYLOAD
        ret['path-parameter-in-url'] = EPInfoIsAlive.PATH_PAR_URL

        ret['parameters'] = [{}]

        return ret

    def executeByParameters(self, epocDate) -> dict:

        payload = {}
        return self.executeByPayload(payload)

    def executeByPayload(self, payload) -> dict:

        remoteAddress = request.remote_addr

        logging.debug( "WEB request ({0}): {1} {2}".format(
                    remoteAddress, EPInfoReady.METHOD, EPInfoReady.URL
                )
        )

        return output_json( {'result': 'OK'}, EP.CODE_OK)

#        logging.debug( "WEB request: {0} {1}".format(
#                    EPInfoReady.METHOD, EPInfoReady.URL
#                )
#        )
#
#        ret = {"result": "OK"}
#        return output_json( ret, EP.CODE_OK)

