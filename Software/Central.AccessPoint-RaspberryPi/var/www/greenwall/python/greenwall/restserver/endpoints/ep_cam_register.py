import logging

from greenwall.exceptions.invalid_api_usage import InvalidAPIUsage
from greenwall.restserver.endpoints.ep import EP
from greenwall.restserver.representations import output_json

from flask import request

from dateutil import parser
from datetime import datetime

class EPCamRegister(EP):

    ID = 'cam_register'
    URL = '/cam/register'

    PATH_PAR_PAYLOAD = '/register'
#    PATH_PAR_URL = '/stream/register/dateString/<dateString>/lampId/<lampId>'

    METHOD = 'POST'

    ATTR_ID = 'camId'
    ATTR_STREAM_URL = 'streamUrl'
    ATTR_CAPTURE_URL = 'captureUrl'
    ATTR_DATE_STRING = 'dateString'

    def __init__(self, web_gadget):
        self.web_gadget = web_gadget

    @staticmethod
    def getRequestDescriptionWithPayloadParameters():

        ret = {}
        ret['camId'] = EPCamRegister.ID
        ret['method'] = EPCamRegister.METHOD
        ret['path-parameter-in-payload'] = EPCamRegister.PATH_PAR_PAYLOAD
#        ret['path-parameter-in-url'] = EPCamCaptureRegister.PATH_PAR_URL

        ret['parameters'] = [{},{},{},{}]

        ret['parameters'][0]['attribute'] = EPCamRegister.ATTR_ID
        ret['parameters'][0]['type'] = 'string'
        ret['parameters'][0]['value'] = 255

        ret['parameters'][1]['attribute'] = EPCamRegister.ATTR_STREAM_URL
        ret['parameters'][1]['type'] = 'string'
        ret['parameters'][1]['value'] = 255

        ret['parameters'][2]['attribute'] = EPCamRegister.ATTR_CAPTURE_URL
        ret['parameters'][2]['type'] = 'string'
        ret['parameters'][2]['value'] = 255

        ret['parameters'][3]['attribute'] = EPCamRegister.ATTR_DATE_STRING
        ret['parameters'][3]['type'] = 'string'
        ret['parameters'][3]['value'] = 255

        return ret

    def executeByParameters(self, camId, streamUrl, captureUrl, dateString) -> dict:
        payload = {}
        payload[EPCamRegister.ATTR_ID] = camId
        payload[EPCamRegister.ATTR_CAPTURE_URL] = captureUrl
        payload[EPCamRegister.ATTR_STREAM_URL] = streamUrl
        payload[EPCamRegister.ATTR_DATE_STRING] = dateString

        return self.executeByPayload(payload)

    def executeByPayload(self, payload) -> dict:

        camId = payload[EPCamRegister.ATTR_ID]
        streamUrl = payload[EPCamRegister.ATTR_STREAM_URL]
        captureUrl = payload[EPCamRegister.ATTR_CAPTURE_URL]
        dateString = payload[EPCamRegister.ATTR_DATE_STRING]

        logging.debug( "WEB request: {0} {1} ('{2}': {3}, '{4}': {5}, '{6}': {7} )".format(
                    EPCamRegister.METHOD, EPCamRegister.URL,
                    EPCamRegister.ATTR_ID, camId,
                    EPCamRegister.ATTR_STREAM_URL, streamUrl,
                    EPCamRegister.ATTR_CAPTURE_URL, captureUrl,
                    EPCamRegister.ATTR_DATE_STRING, dateString
                    )
            )

        date = parser.parse(dateString)
        dateString = date.astimezone().isoformat()

        camIp = request.remote_addr

        self.web_gadget.registerCam.register(dateString, camIp, camId, streamUrl, captureUrl)

        # print out to LCD
#        self.web_gadget.controlBox.refreshData(stationId)

        return output_json( {'result': 'OK'}, EP.CODE_OK)

