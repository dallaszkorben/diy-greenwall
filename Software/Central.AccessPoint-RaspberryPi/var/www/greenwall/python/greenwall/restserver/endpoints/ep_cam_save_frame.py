import os
from pathlib import Path

import logging

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

class EPCamSaveFrame(EP):

    ID = 'cam_save_frame'
    URL = '/cam/save/frame'

    PATH_PAR_PAYLOAD = '/save/frame'
    PATH_PAR_URL = '/save/frame/camId/<camId>'

    METHOD = 'POST'

    ATTR_CAM_ID = 'camId'
    ATTR_IMAGE = 'image'


    def __init__(self, web_gadget):
        self.web_gadget = web_gadget

        self.lockExecuteSave = Lock()

    @staticmethod
    def getRequestDescriptionWithPayloadParameters():

        ret = {}
        ret['id'] = EPCamSaveFrame.ID
        ret['method'] = EPCamSaveFrame.METHOD
        ret['path-parameter-in-payload'] = EPCamSaveFrame.PATH_PAR_PAYLOAD
        ret['path-parameter-in-url'] = EPCamSaveFrame.PATH_PAR_URL

        ret['parameters'] = [{},{}]

        ret['parameters'][0]['attribute'] = EPCamSaveFrame.ATTR_CAM_ID
        ret['parameters'][0]['type'] = 'string'
        ret['parameters'][0]['value'] = 255

        return ret

    def executeByParameters(self, camId, image=None) -> dict:
        payload = {}
        payload[EPCamSaveFrame.ATTR_CAM_ID] = camId
        payload[EPCamSaveFrame.ATTR_IMAGE] = image

        with self.lockExecuteSave:
            return self.executeByPayload(payload)

    def executeByPayload(self, payload) -> dict:

        camId = payload[EPCamSaveFrame.ATTR_CAM_ID]
        image = payload[EPCamSaveFrame.ATTR_IMAGE]

        logging.debug( "   REST request was received: {0} {1} ('{2}': {3}, '{4}': {5})".format(
                EPCamSaveFrame.METHOD, EPCamSaveFrame.URL,
                EPCamSaveFrame.ATTR_CAM_ID, camId,
                EPCamSaveFrame.ATTR_IMAGE, image ))

        dateString = datetime.now().astimezone().isoformat()



        absoluteRootPath = self.web_gadget.absoluteRootPath
        webCamFrameFolder = self.web_gadget.webCamFrameFolder

        fileName = f'{dateString}.jpg'
        # constract the path /var/www/greenwall/cam-frame/5
        path = os.path.join(absoluteRootPath, webCamFrameFolder, camId)
        fileNamePath = os.path.join(path, fileName)

        if image:

            # Create the path if it dees not exist
            Path(path).mkdir(parents=True, exist_ok=True)

            img = Image.open(image)

            try:
                # add timestamp to the image
                draw = ImageDraw.Draw(img)
            except Exception as e:
                logging.debug("      {0} FRAME was NOT saved. ImageDraw FAILE\n{1}".format(fileNamePath,e))
                return output_json( {'result': 'ERROR'}, EP.CODE_BAD_REQUEST)

            font = ImageFont.truetype("DejaVuSans.ttf", 32)
            draw.text((0,20), dateString, (100,100,100), font=font)

            img.save(fileNamePath)

            logging.debug("      {0} FRAME was saved".format(fileNamePath))
            return output_json( {'result': 'OK'}, EP.CODE_OK)

        else:

            logging.error( "      !!! No {0} was saved as there was NO image sent) !!!".format(fileNamePath))
            return output_json( {'result': 'ERROR'}, EP.CODE_BAD_REQUEST)



