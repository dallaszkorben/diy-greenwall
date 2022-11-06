import logging

from greenwall.exceptions.invalid_api_usage import InvalidAPIUsage
from greenwall.restserver.endpoints.ep import EP
from greenwall.restserver.representations import output_json

from flask import request

from dateutil import parser
from datetime import datetime

class EPSensorRegisteredList(EP):

    ID = 'sensor_configure'
    URL = '/sensor/registered/list'

    PATH_PAR_PAYLOAD = '/registered/list'
    PATH_PAR_URL = '/registered/list'

    METHOD = 'GET'

    def __init__(self, web_gadget):
        self.web_gadget = web_gadget

    @staticmethod
    def getRequestDescriptionWithPayloadParameters():

        ret = {}
        ret['id'] = EPSensorRegisteredList.ID
        ret['method'] = EPSensorRegisteredList.METHOD
        ret['path-parameter-in-payload'] = EPSensorRegisteredList.PATH_PAR_PAYLOAD
        ret['path-parameter-in-url'] = EPSensorRegisteredList.PATH_PAR_URL

        ret['parameters'] = []

        return ret

    def executeByParameters(self) -> dict:
        payload = {}

        return self.executeByPayload(payload)

    def executeByPayload(self, payload) -> dict:

        remoteAddress = request.remote_addr

        logging.debug( "WEB request ({0}): {1} {2} ()".format(
                    remoteAddress, EPSensorRegisteredList.METHOD, EPSensorRegisteredList.URL,
                    )
        )

        # Get the registered station list
        # [
        # {'stationId': 'S01', 'stationIp': '192.168.50.40'},
        # {'stationId': 'S02', 'stationIp': '192.168.50.112'},
        # ]
        ret = self.web_gadget.registerSensor.getValueList()

        # If not empty
        #if ret:
        return output_json(ret, EP.CODE_OK)
        #else:
        #    return output_json( ret, EP.CODE_INTERNAL_SERVER_ERROR)
