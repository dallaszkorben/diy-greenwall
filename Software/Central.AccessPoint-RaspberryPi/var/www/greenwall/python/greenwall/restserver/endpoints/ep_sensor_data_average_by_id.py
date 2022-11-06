import logging

from greenwall.exceptions.invalid_api_usage import InvalidAPIUsage
from greenwall.restserver.endpoints.ep import EP
from greenwall.restserver.representations import output_json

from flask import request

from dateutil import parser
from datetime import datetime

class EPSensorDataAverageById(EP):

    ID = 'sensor_data_average'
    URL = '/sensor/data/average'

    PATH_PAR_PAYLOAD = '/data/average'
    PATH_PAR_URL = '/data/average/id/<id>'

    METHOD = 'GET'

    ATTR_ID = 'id'

    def __init__(self, web_gadget):
        self.web_gadget = web_gadget

    @staticmethod
    def getRequestDescriptionWithPayloadParameters():

        ret = {}
        ret['id'] = EPSensorDataAverageById.ID
        ret['method'] = EPSensorDataAverageById.METHOD
        ret['path-parameter-in-payload'] = EPSensorDataAverageById.PATH_PAR_PAYLOAD
        ret['path-parameter-in-url'] = EPSensorDataAverageById.PATH_PAR_URL

        ret['parameters'] = [{}]

        ret['parameters'][0]['attribute'] = EPSensorDataAverageById.ATTR_ID
        ret['parameters'][0]['type'] = 'string'
        ret['parameters'][0]['value'] = 255

        return ret

    def executeByParameters(self, id) -> dict:
        payload = {}

        payload[EPSensorDataAverageById.ATTR_ID] = id

        return self.executeByPayload(payload)

    def executeByPayload(self, payload) -> dict:

        stationId = payload[EPSensorDataAverageById.ATTR_ID]

        remoteAddress = request.remote_addr

        logging.debug( "WEB request ({0}): {1} {2} ('{3}': {4})".format(
                    remoteAddress, EPSensorDataAverageById.METHOD, EPSensorDataAverageById.URL,
                    EPSensorDataAverageById.ATTR_ID, stationId
                    )
        )

        average = self.web_gadget.sensor.getAverage(stationId)

        if average["success"] == True:
            return output_json( average, EP.CODE_OK)
        else:
            return output_json( average, EP.CODE_INTERNAL_SERVER_ERROR)


