import logging

from greenwall.exceptions.invalid_api_usage import InvalidAPIUsage
from greenwall.restserver.endpoints.ep import EP
from greenwall.restserver.representations import output_json

from flask import request

from dateutil import parser
from datetime import datetime

class EPPumpStatus(EP):

    ID = 'pump_status'
    URL = '/pump/status'

    PATH_PAR_PAYLOAD = '/status'
    PATH_PAR_URL = '/status'

    METHOD = 'GET'

    def __init__(self, web_gadget):
        self.web_gadget = web_gadget

    @staticmethod
    def getRequestDescriptionWithPayloadParameters():

        ret = {}
        ret['id'] = EPPumpStatus.ID
        ret['method'] = EPPumpStatus.METHOD
        ret['path-parameter-in-payload'] = EPPumpStatus.PATH_PAR_PAYLOAD
        ret['path-parameter-in-url'] = EPPumpStatus.PATH_PAR_URL

        ret['parameters'] = []

        return ret

    def executeByParameters(self) -> dict:
        payload = {}

        return self.executeByPayload(payload)

    def executeByPayload(self, payload) -> dict:

        logging.debug( "WEB request: {0} {1} ()".format(
                    EPPumpStatus.METHOD, EPPumpStatus.URL
                    )
            )

        status = self.web_gadget.pump.getPumpStatus()

        return output_json( {'result': 'OK', 'status': status}, EP.CODE_OK)

