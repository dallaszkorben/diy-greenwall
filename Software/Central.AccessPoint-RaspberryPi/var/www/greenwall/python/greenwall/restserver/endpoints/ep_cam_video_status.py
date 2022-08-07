import logging
import threading
from pathlib import Path

from greenwall.exceptions.invalid_api_usage import InvalidAPIUsage
from greenwall.restserver.endpoints.ep import EP
from greenwall.restserver.representations import output_json

from flask import request

from dateutil import parser
from datetime import datetime

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 

from threading import Lock

import cv2
import os
from natsort import natsorted

class EPCamVideoStatus(EP):

    ID = 'cam_video_status'
    URL = '/cam/video/status'

    PATH_PAR_PAYLOAD = '/video/status'
    PATH_PAR_URL = '/video/status'

    METHOD = 'GET'

    def __init__(self, web_gadget):
        self.web_gadget = web_gadget

    @staticmethod
    def getRequestDescriptionWithPayloadParameters():

        ret = {}
        ret['id'] = EPCamVideoStatus.ID
        ret['method'] = EPCamVideoStatus.METHOD
        ret['path-parameter-in-payload'] = EPCamVideoStatus.PATH_PAR_PAYLOAD
        ret['path-parameter-in-url'] = EPCamVideoStatus.PATH_PAR_URL

        ret['parameters'] = []

        return ret

    def executeByParameters(self) -> dict:
        payload = {}

        return self.executeByPayload(payload)

    def executeByPayload(self, payload) -> dict:

        logging.debug( "   REST request was received: {0} {1} ()".format(
                EPCamVideoStatus.METHOD, EPCamVideoStatus.URL ))

        ret = self.web_gadget.cam.getProgressVideoConstruct()
        ret["result"] = "OK"
        return output_json( ret, EP.CODE_OK)


