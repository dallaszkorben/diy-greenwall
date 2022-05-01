import logging
from exceptions.invalid_api_usage import InvalidAPIUsage
from restserver.endpoints.ep import EP
from restserver.representations import output_json

from flask import request

from dateutil import parser
from datetime import datetime

class EPCamStreamRegister(EP):

    ID = 'cam_stream_register'
    URL = '/cam/stream/register'

    PATH_PAR_PAYLOAD = '/stream/register'
#    PATH_PAR_URL = '/stream/register/dateString/<dateString>/lampId/<lampId>'

    METHOD = 'POST'

    ATTR_ID = 'id'
    ATTR_URL = 'url'
    ATTR_DATE_STRING = 'dateString'

    def __init__(self, web_gadget):
        self.web_gadget = web_gadget

    @staticmethod
    def getRequestDescriptionWithPayloadParameters():

        ret = {}
        ret['id'] = EPCamStreamRegister.ID
        ret['method'] = EPCamStreamRegister.METHOD
        ret['path-parameter-in-payload'] = EPCamStreamRegister.PATH_PAR_PAYLOAD
#        ret['path-parameter-in-url'] = EPCamStreamRegister.PATH_PAR_URL

        ret['parameters'] = [{},{},{}]

        ret['parameters'][0]['attribute'] = EPCamStreamRegister.ATTR_ID
        ret['parameters'][0]['type'] = 'string'
        ret['parameters'][0]['value'] = 255

        ret['parameters'][1]['attribute'] = EPCamStreamRegister.ATTR_URL
        ret['parameters'][1]['type'] = 'string'
        ret['parameters'][1]['value'] = 255

        ret['parameters'][2]['attribute'] = EPCamStreamRegister.ATTR_DATE_STRING
        ret['parameters'][2]['type'] = 'string'
        ret['parameters'][2]['value'] = 255

        return ret

    def executeByParameters(self, id, url, dateString) -> dict:
        payload = {}
        payload[EPCamStreamRegister.ATTR_ID] = id
        payload[EPCamStreamRegister.ATTR_URL] = url
        payload[EPCamStreamRegister.ATTR_DATE_STRING] = dateString

        return self.executeByPayload(payload)

    def executeByPayload(self, payload) -> dict:

        camStreamId = payload[EPCamStreamRegister.ATTR_ID]
        camStreamUrl = payload[EPCamStreamRegister.ATTR_URL]
        dateString = payload[EPCamStreamRegister.ATTR_DATE_STRING]



        logging.debug( "WEB request: {0} {1} ('{2}': {3}, '{4}': {5} )".format(
                    EPCamStreamRegister.METHOD, EPCamStreamRegister.URL,
                    EPCamStreamRegister.ATTR_ID, camStreamId,
                    EPCamStreamRegister.ATTR_URL, camStreamUrl,
                    EPCamStreamRegister.ATTR_DATE_STRING, dateString
                    )
            )

        date = parser.parse(dateString)
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

        camStreamIp = request.remote_addr

        self.web_gadget.registerCamStream.register(dateString, camStreamIp, camStreamId, camStreamUrl)

        # print out to LCD
#        self.web_gadget.controlBox.refreshData(stationId)

        return output_json( {'result': 'OK'}, EP.CODE_OK)

