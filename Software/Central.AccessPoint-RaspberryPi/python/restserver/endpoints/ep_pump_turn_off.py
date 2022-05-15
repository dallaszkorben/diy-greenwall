import logging
from exceptions.invalid_api_usage import InvalidAPIUsage
from restserver.endpoints.ep import EP
from restserver.representations import output_json

from flask import request

from dateutil import parser
from datetime import datetime

class EPPumpTurnOff(EP):

    ID = 'pump_turn_off'
    URL = '/lamp/turnOff'

    PATH_PAR_PAYLOAD = '/turnOff'
    PATH_PAR_URL = '/turnOff'

    METHOD = 'POST'

    def __init__(self, web_gadget):
        self.web_gadget = web_gadget

    @staticmethod
    def getRequestDescriptionWithPayloadParameters():

        ret = {}
        ret['id'] = EPPumpTurnOff.ID
        ret['method'] = EPPumpTurnOff.METHOD
        ret['path-parameter-in-payload'] = EPPumpTurnOff.PATH_PAR_PAYLOAD
        ret['path-parameter-in-url'] = EPPumpTurnOff.PATH_PAR_URL

        ret['parameters'] = []

        return ret

    def executeByParameters(self) -> dict:
        payload = {}

        return self.executeByPayload(payload)

    def executeByPayload(self, payload) -> dict:

        logging.debug( "WEB request: {0} {1} ()".format(
                    EPPumpTurnOff.METHOD, EPPumpTurnOff.URL
                    )
            )


        self.web_gadget.pump.turnPumpOff()

        return output_json( {'result': 'OK'}, EP.CODE_OK)

