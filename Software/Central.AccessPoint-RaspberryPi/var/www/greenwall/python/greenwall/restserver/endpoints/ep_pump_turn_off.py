import logging

from greenwall.exceptions.invalid_api_usage import InvalidAPIUsage
from greenwall.restserver.endpoints.ep import EP
from greenwall.restserver.representations import output_json

from flask import request

from dateutil import parser
from datetime import datetime

class EPPumpTurnOff(EP):

    ID = 'pump_turn_off'
    URL = '/pump/turnOff'

    PATH_PAR_PAYLOAD = '/turnOff'
    PATH_PAR_URL = '/turnOff/ip/<ip>'

    METHOD = 'POST'

    ATTR_IP = 'ip'

    def __init__(self, web_gadget):
        self.web_gadget = web_gadget

    @staticmethod
    def getRequestDescriptionWithPayloadParameters():

        ret = {}
        ret['id'] = EPPumpTurnOff.ID
        ret['method'] = EPPumpTurnOff.METHOD
        ret['path-parameter-in-payload'] = EPPumpTurnOff.PATH_PAR_PAYLOAD
        ret['path-parameter-in-url'] = EPPumpTurnOff.PATH_PAR_URL

        ret['parameters'] = [{}]

        ret['parameters'][0]['attribute'] = EPPumpTurnOff.ATTR_IP
        ret['parameters'][0]['type'] = 'string'
        ret['parameters'][0]['value'] = 255

        return ret

    def executeByParameters(self, ip) -> dict:
        payload = {}
        payload[EPPumpTurnOff.ATTR_IP] = ip

        return self.executeByPayload(payload)

    def executeByPayload(self, payload) -> dict:

        ip = payload[EPPumpTurnOff.ATTR_IP]

        remoteAddress = request.remote_addr

        logging.debug( "WEB request ({0}): {1} {2} ('{3}': {4})".format(
                    remoteAddress, EPPumpTurnOff.METHOD, EPPumpTurnOff.URL,
                    EPPumpTurnOff.ATTR_IP, ip
                    )
            )


        self.web_gadget.pump.turnPumpOff(ip)

        return output_json( {'result': 'OK'}, EP.CODE_OK)
