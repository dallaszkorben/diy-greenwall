import logging
from exceptions.invalid_api_usage import InvalidAPIUsage
from restserver.endpoints.ep import EP
from restserver.representations import output_json

from flask import request

from dateutil import parser
from datetime import datetime

class EPLampStatus(EP):

    ID = 'lamp_status'
    URL = '/lamp/status'

    PATH_PAR_PAYLOAD = '/status'
    PATH_PAR_URL = '/status'

    METHOD = 'GET'

    def __init__(self, web_gadget):
        self.web_gadget = web_gadget

    @staticmethod
    def getRequestDescriptionWithPayloadParameters():

        ret = {}
        ret['id'] = EPLampStatus.ID
        ret['method'] = EPLampStatus.METHOD
        ret['path-parameter-in-payload'] = EPLampStatus.PATH_PAR_PAYLOAD
        ret['path-parameter-in-url'] = EPLampStatus.PATH_PAR_URL

        ret['parameters'] = []

        return ret

    def executeByParameters(self) -> dict:
        payload = {}

        return self.executeByPayload(payload)

    def executeByPayload(self, payload) -> dict:

        logging.debug( "WEB request: {0} {1} ()".format(
                    EPLampStatus.METHOD, EPLampStatus.URL
                    )
            )

        status = self.web_gadget.lamp.getLampStatus()

#        self.web_gadget.lamp.turnLampOn(lengthInSec)
#
#
#        if status == "on":
#            self.web_gadget.lamp.turnLampOn(lengthInSec)
#        else:
#            self.web_gadget.lamp.turnLampOff(lengthInSec)

        # print out to LCD
#        self.web_gadget.controlBox.refreshData(stationId)

        return output_json( {'result': 'OK', 'status': status}, EP.CODE_OK)

