import logging

from greenwall.exceptions.invalid_api_usage import InvalidAPIUsage
from greenwall.restserver.endpoints.ep import EP
from greenwall.restserver.representations import output_json

from flask import request

from dateutil import parser
from datetime import datetime

class EPLampSwitch(EP):

    ID = 'lamp_switch'
    URL = '/lamp/switch'

    PATH_PAR_PAYLOAD = '/switch'
    PATH_PAR_URL = '/switch/status/<status>/lengthInSec/<lengthInSec>'

    METHOD = 'POST'

    ATTR_STATUS = 'status'
    ATTR_LENGTH_IN_SEC = 'lengthInSec'

    def __init__(self, web_gadget):
        self.web_gadget = web_gadget

    @staticmethod
    def getRequestDescriptionWithPayloadParameters():

        ret = {}
        ret['id'] = EPLampSwitch.ID
        ret['method'] = EPLampSwitch.METHOD
        ret['path-parameter-in-payload'] = EPLampSwitch.PATH_PAR_PAYLOAD
        ret['path-parameter-in-url'] = EPLampSwitch.PATH_PAR_URL

        ret['parameters'] = [{},{}]

        ret['parameters'][0]['attribute'] = EPLampSwitch.ATTR_STATUS
        ret['parameters'][0]['type'] = 'string'
        ret['parameters'][0]['value'] = 255

        ret['parameters'][1]['attribute'] = EPLampSwitch.ATTR_LENGTH_IN_SEC
        ret['parameters'][1]['type'] = 'string'
        ret['parameters'][1]['value'] = 255

        return ret

    def executeByParameters(self, status, lengthInSec) -> dict:
        payload = {}
        payload[EPLampSwitch.ATTR_STATUS] = status
        payload[EPLampSwitch.ATTR_LENGTH_IN_SEC] = lengthInSec

        return self.executeByPayload(payload)

    def executeByPayload(self, payload) -> dict:

        status = payload[EPLampSwitch.ATTR_STATUS]
        lengthInSec = payload[EPLampSwitch.ATTR_LENGTH_IN_SEC]

        logging.debug( "WEB request: {0} {1} ('{2}': {3} )".format(
                    EPLampSwitch.METHOD, EPLampSwitch.URL,
                    EPLampSwitch.ATTR_STATUS, status,
                    EPLampSwitch.ATTR_LENGTH_IN_SEC, lengthInSec
                    )
            )


        if status == "on":
            self.web_gadget.lamp.turnLampOn(lengthInSec)
        else:
            self.web_gadget.lamp.turnLampOff(lengthInSec)

        # print out to LCD
#        self.web_gadget.controlBox.refreshData(stationId)

        return output_json( {'result': 'OK'}, EP.CODE_OK)

