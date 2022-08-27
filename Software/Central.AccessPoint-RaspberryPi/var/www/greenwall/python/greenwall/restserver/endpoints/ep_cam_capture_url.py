import logging

from greenwall.exceptions.invalid_api_usage import InvalidAPIUsage
from greenwall.restserver.endpoints.ep import EP
from greenwall.restserver.representations import output_json

from flask import request

from dateutil import parser
from datetime import datetime

class EPCamCaptureUrl(EP):

    ID = 'cam_capture_url'
    URL = '/cam/capture/url'

    PATH_PAR_PAYLOAD = '/capture/url'
    PATH_PAR_URL = '/capture/url/camId/<camId>'

    METHOD = 'GET'

    ATTR_ID = 'camId'

    def __init__(self, web_gadget):
        self.web_gadget = web_gadget

    @staticmethod
    def getRequestDescriptionWithPayloadParameters():

        ret = {}
        ret['id'] = EPCamCaptureUrl.ID
        ret['method'] = EPCamCaptureUrl.METHOD
        ret['path-parameter-in-payload'] = EPCamCaptureUrl.PATH_PAR_PAYLOAD
        ret['path-parameter-in-url'] = EPCamCaptureUrl.PATH_PAR_URL

        ret['parameters'] = [{}]

        ret['parameters'][0]['attribute'] = EPCamCaptureUrl.ATTR_ID
        ret['parameters'][0]['type'] = 'string'
        ret['parameters'][0]['value'] = 255

        return ret

    def executeByParameters(self, camId) -> dict:
        payload = {}
        payload[EPCamCaptureUrl.ATTR_ID] = camId

        return self.executeByPayload(payload)

    def executeByPayload(self, payload) -> dict:

        camId = payload[EPCamCaptureUrl.ATTR_ID]

        remoteAddress = request.remote_addr

        logging.debug( "WEB request ({0}): {1} {2} ('{3}': {4} )".format(
                    remoteAddress, EPCamCaptureUrl.METHOD, EPCamCaptureUrl.URL,
                    EPCamCaptureUrl.ATTR_ID, camId
                    )
        )

        # Take picture and save it into WebCamCapture folder
        captureUrl = self.web_gadget.cam.getCapture(camId)

        return output_json( {'result': 'OK', 'captureUrl': captureUrl}, EP.CODE_OK)

