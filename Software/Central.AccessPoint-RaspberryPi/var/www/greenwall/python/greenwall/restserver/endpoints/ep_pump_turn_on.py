import logging

from greenwall.exceptions.invalid_api_usage import InvalidAPIUsage
from greenwall.restserver.endpoints.ep import EP
from greenwall.restserver.representations import output_json

from flask import request

from dateutil import parser
from datetime import datetime

class EPPumpTurnOn(EP):

    ID = 'pump_turn_on'
    URL = '/lamp/turnOn'

    PATH_PAR_PAYLOAD = '/turnOn'
    PATH_PAR_URL = '/turnOn/lengthInSec/<lengthInSec>'

    METHOD = 'POST'

    ATTR_LENGTH_IN_SEC = 'lengthInSec'

    def __init__(self, web_gadget):
        self.web_gadget = web_gadget

    @staticmethod
    def getRequestDescriptionWithPayloadParameters():

        ret = {}
        ret['id'] = EPPumpTurnOn.ID
        ret['method'] = EPPumpTurnOn.METHOD
        ret['path-parameter-in-payload'] = EPPumpTurnOn.PATH_PAR_PAYLOAD
        ret['path-parameter-in-url'] = EPPumpTurnOn.PATH_PAR_URL

        ret['parameters'] = [{}]

        ret['parameters'][0]['attribute'] = EPPumpTurnOn.ATTR_LENGTH_IN_SEC
        ret['parameters'][0]['type'] = 'string'
        ret['parameters'][0]['value'] = 255

        return ret

    def executeByParameters(self, lengthInSec) -> dict:
        payload = {}
        payload[EPPumpTurnOn.ATTR_LENGTH_IN_SEC] = lengthInSec

        return self.executeByPayload(payload)

    def executeByPayload(self, payload) -> dict:

        lengthInSec = payload[EPPumpTurnOn.ATTR_LENGTH_IN_SEC]

        remoteAddress = request.remote_addr

        logging.debug( "WEB request ({0}): {1} {2} ('{3}': {4} )".format(
                    remoteAddress, EPPumpTurnOn.METHOD, EPPumpTurnOn.URL,
                    EPPumpTurnOn.ATTR_LENGTH_IN_SEC, lengthInSec
                    )
            )


        self.web_gadget.pump.turnPumpOn(lengthInSec)

        return output_json( {'result': 'OK'}, EP.CODE_OK)

