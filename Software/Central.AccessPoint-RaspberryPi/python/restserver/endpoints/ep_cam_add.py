import logging
from exceptions.invalid_api_usage import InvalidAPIUsage
from restserver.endpoints.ep import EP
from restserver.representations import output_json

from flask import request

from dateutil import parser
from datetime import datetime

class EPCamAdd(EP):

    ID = 'cam_add'
    URL = '/cam/add'

    PATH_PAR_PAYLOAD = '/add'
    PATH_PAR_URL = '/add/camId/<camId>/timestamp/<timestamp>'

    METHOD = 'POST'

    ATTR_CAM_ID = 'camId'
    ATTR_TIMESTAMP = 'timestamp'

    def __init__(self, web_gadget):
        self.web_gadget = web_gadget

    @staticmethod
    def getRequestDescriptionWithPayloadParameters():

        ret = {}
        ret['id'] = EPCamAdd.ID
        ret['method'] = EPCamAdd.METHOD
        ret['path-parameter-in-payload'] = EPCamAdd.PATH_PAR_PAYLOAD
        ret['path-parameter-in-url'] = EPCamAdd.PATH_PAR_URL

        ret['parameters'] = [{},{},{}]

        ret['parameters'][0]['attribute'] = EPCamAdd.ATTR_CAM_ID
        ret['parameters'][0]['type'] = 'string'
        ret['parameters'][0]['value'] = 255

        ret['parameters'][1]['attribute'] = EPCamAdd.ATTR_TIMESTAMP
        ret['parameters'][1]['type'] = 'string'
        ret['parameters'][1]['value'] = 255

        return ret

    def executeByParameters(self, camId, timestamp) -> dict:
        payload = {}
        payload[EPCamAdd.ATTR_CAM_ID] = camId
        payload[EPCamAdd.ATTR_TIMESTAMP] = timestamp

        return self.executeByPayload(payload)

    def executeByPayload(self, payload) -> dict:

        camId = payload[EPCamAdd.ATTR_CAM_ID]
        timestamp = payload[EPCamAdd.ATTR_TIMESTAMP]

        logging.debug( "WEB request: {0} {1} ('{2}': {3}, '{4}': {5})".format(
                    EPCamAdd.METHOD, EPCamAdd.URL,
                    EPCamAdd.ATTR_CAM_ID, camId,
                    EPCamAdd.ATTR_TIMESTAMP, timestamp,
                    )
            )

#        dateString = datetime.now().astimezone().isoformat()
#        dateString = datetime.datetime.now().astimezone().isoformat()

        date = parser.parse(timestamp)
        dateString = date.astimezone().isoformat()


# datetime now()
#  datetime.datetime.now().astimezone()
#
# String now()
#  datetime.datetime.now().astimezone().isoformat()
#
# datetime from String
#    date = parser.parse(dateString)
#
# timestamp from datetime
#    timeStamp = date.timestamp()
#    timeStamp = datetime.timestamp(date)
#
# datetime from timestamp
#    datetime.fromtimestamp(timeStamp)

        ip = request.remote_addr

        # Report Log

        # Add to reportDict
#        self.web_gadget.reportSensor.addRecordSensor(dateString, stationId, ip, levelValue, levelVariance, temperatureValue, humidityValue)

        # print out to LCD
#        self.web_gadget.controlBox.refreshData(stationId)

        return output_json( {'result': 'OK'}, EP.CODE_OK)

