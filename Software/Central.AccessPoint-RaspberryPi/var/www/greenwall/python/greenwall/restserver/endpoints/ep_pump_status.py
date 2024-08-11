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
    PATH_PAR_URL = '/status/ip/<ip>'

    ATTR_IP = 'ip'

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

    def executeByParameters(self, ip) -> dict:
        payload = {}
        payload[EPPumpStatus.ATTR_IP] = ip

        return self.executeByPayload(payload)

    def executeByPayload(self, payload) -> dict:

        remoteAddress = request.remote_addr
        ip = payload[EPPumpStatus.ATTR_IP]

        logging.debug( "WEB request ({0}): {1} {2} ({3}': '{4}')".format(
                    remoteAddress, EPPumpStatus.METHOD, EPPumpStatus.URL,
                    EPPumpStatus.ATTR_IP, ip
                    )
            )

        data = self.web_gadget.pump.getPumpStatus(ip)

        return output_json( {'result': 'OK', 'data': data}, EP.CODE_OK)
