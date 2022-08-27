import logging

from greenwall.exceptions.invalid_api_usage import InvalidAPIUsage
from greenwall.restserver.endpoints.ep import EP
from greenwall.utilities.register_cam import RegisterCam
from greenwall.restserver.representations import output_json

from flask import request

from dateutil import parser
from datetime import datetime

import numpy as np

from scipy import stats

class EPCamCaptureList(EP):

    ID = 'cam_captureList'
    URL = '/cam/captureList'

    PATH_PAR_PAYLOAD = '/captureList'
    PATH_PAR_URL = '/captureList'

    METHOD = 'GET'

    def __init__(self, web_gadget):
        self.web_gadget = web_gadget

    @staticmethod
    def getRequestDescriptionWithPayloadParameters():

        ret = {}
        ret['id'] = EPCamCaptureList.ID
        ret['method'] = EPInfoCamCaptureList.METHOD
        ret['path-parameter-in-payload'] = EPCamCaptureList.PATH_PAR_PAYLOAD
        ret['path-parameter-in-url'] = EPCamCaptureList.PATH_PAR_URL

        ret['parameters'] = []

        return ret

    def executeByParameters(self) -> dict:

        payload = {}
        return self.executeByPayload(payload)

    def executeByPayload(self, payload) -> dict:

        remoteAddress = request.remote_addr

        logging.debug( "WEB request ({0}): {1} {2} ()".format(
                    remoteAddress if remoteAddress else "", EPCamCaptureList.METHOD, EPCamCaptureList.URL,
                )
        )

        camCaptureList = self.web_gadget.registerCam.getValueList(capture=True)

        ret = {"result": "OK", "camCaptureList": camCaptureList}
        return output_json( ret, EP.CODE_OK)

