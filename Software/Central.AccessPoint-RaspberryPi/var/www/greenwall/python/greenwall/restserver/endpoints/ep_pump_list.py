import logging

from greenwall.exceptions.invalid_api_usage import InvalidAPIUsage
from greenwall.restserver.endpoints.ep import EP
from greenwall.restserver.representations import output_json

from flask import request

from dateutil import parser
from datetime import datetime

class EPPumpList(EP):

    ID = 'pump_list'
    URL = '/pump/list'

    PATH_PAR_PAYLOAD = '/list'
    PATH_PAR_URL = '/list'

    METHOD = 'GET'

    def __init__(self, web_gadget):
        self.web_gadget = web_gadget

    @staticmethod
    def getRequestDescriptionWithPayloadParameters():

        ret = {}
        ret['id'] = EPPumpList.ID
        ret['method'] = EPPumpList.METHOD
        ret['path-parametser-in-payload'] = EPPumpList.PATH_PAR_PAYLOAD
        ret['path-parameter-in-url'] = EPPumpList.PATH_PAR_URL

        ret['parameters'] = []

        return ret

    def executeByParameters(self) -> dict:
        payload = {}

        return self.executeByPayload(payload)

    def executeByPayload(self, payload) -> dict:

        remoteAddress = request.remote_addr

        logging.debug( "WEB request ({0}): {1} {2} ()".format(
                    remoteAddress, EPPumpList.METHOD, EPPumpList.URL
                    )
            )

        pump_list = self.web_gadget.pump.getPumpList()

        return output_json( {'result': 'OK', 'pump-list': pump_list}, EP.CODE_OK)

