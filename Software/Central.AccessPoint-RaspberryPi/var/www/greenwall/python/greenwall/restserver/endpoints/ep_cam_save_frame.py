import os
from pathlib import Path

import logging

from greenwall.exceptions.invalid_api_usage import InvalidAPIUsage
from greenwall.restserver.endpoints.ep import EP
from greenwall.restserver.representations import output_json

from flask import request

from dateutil import parser
from datetime import datetime
import time

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 

from threading import Lock

class EPCamSaveFrame(EP):

    ID = 'cam_save_frame'
    URL = '/cam/save/frame'

    PATH_PAR_PAYLOAD = '/save/frame'
    PATH_PAR_URL = '/save/frame/camId/<camId>/camRotate/<camRotate>'

    METHOD = 'POST'

    ATTR_CAM_ID = 'camId'
    ATTR_CAM_ROTATE = 'camRotate'
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

        ret['parameters'][1]['attribute'] = EPCamSaveFrame.ATTR_CAM_ROTATE
        ret['parameters'][1]['type'] = 'string'
        ret['parameters'][1]['value'] = 255

        return ret

    def executeByParameters(self, camId, camRotate='0', image=None) -> dict:
        payload = {}
        payload[EPCamSaveFrame.ATTR_CAM_ID] = camId
        payload[EPCamSaveFrame.ATTR_CAM_ROTATE] = camRotate
        payload[EPCamSaveFrame.ATTR_IMAGE] = image

        with self.lockExecuteSave:
            return self.executeByPayload(payload)

    def executeByPayload(self, payload) -> dict:

        camId = payload[EPCamSaveFrame.ATTR_CAM_ID]
        camRotate = payload[EPCamSaveFrame.ATTR_CAM_ROTATE]
        image = payload[EPCamSaveFrame.ATTR_IMAGE]

        logging.debug( "   REST request was received: {0} {1} ('{2}': {3}, {4}': {5}, '{6}': {7})".format(
                EPCamSaveFrame.METHOD, EPCamSaveFrame.URL,
                EPCamSaveFrame.ATTR_CAM_ID, camId,
                EPCamSaveFrame.ATTR_CAM_ROTATE, camRotate,
                EPCamSaveFrame.ATTR_IMAGE, image ))

        # 2022-07-29T23:59:55.960950+02:00
        #dateString = datetime.now().astimezone().isoformat()
        # 2022-07-29T23:59:55+02:00
        dateString = time.strftime("%Y-%m-%dT%H:%M:%S%z")

        absoluteRootPath = self.web_gadget.absoluteRootPath

        # constract the frame-file path to /var/www/greenwall/cam-frame/5
        webCamFrameFolder = self.web_gadget.webCamFrameFolder
        frameFileName = f'{dateString}.jpg'
        framePath = os.path.join(absoluteRootPath, webCamFrameFolder, camId)
        frameFileNamePath = os.path.join(framePath, frameFileName)

        # constract the capture-file path to /var/www/greenwall/capture
        webCamCaptureFolder = self.web_gadget.webCamCaptureFolder
        captureFileName = self.web_gadget.webCamCaptureFile.format(camId)
        capturePath = os.path.join(absoluteRootPath, webCamCaptureFolder)
        captureFileNamePath = os.path.join(capturePath, captureFileName)

        if image:

            #
            # Save image as FRAME
            #

            img = Image.open(image)

            # cam rotate
            #0
            # 1
            if camRotate == "1":
                img = img.rotate(-90)
            # 2
            elif camRotate == "2":
                img = img.rotate(-180)
            # 3
            elif camRotate == "3":
                img = img.rotate(-270)

            width, height = img.size

            fontSize = height // 16
            textVPos = height // 32
            textHPos = height // 64

            try:
                # add timestamp to the image
                draw = ImageDraw.Draw(img)
            except Exception as e:
                logging.error("      {0} FRAME/CAPTURE was NOT saved. ImageDraw FAILE\n{1}".format(frameFileNamePath,e))
                return output_json( {'result': 'ERROR'}, EP.CODE_BAD_REQUEST)

            font = ImageFont.truetype("DejaVuSans.ttf", fontSize)
            x=textHPos
            y=textVPos
            outlineAmount=3
            #raw.text((0,20), dateString, (100,100,100), font=font)
            draw.text((x-1, y), dateString, font=font, fill="white")
            draw.text((x+1, y), dateString, font=font, fill="white")
            draw.text((x, y-1), dateString, font=font, fill="white")
            draw.text((x, y+1), dateString, font=font, fill="white")

            draw.text((x, y), dateString, (100,100,100), font=font)

            # ---

            # Create the path for FRAME if it dees not exist
            Path(framePath).mkdir(parents=True, exist_ok=True)

            # Save FRAME
            img.save(frameFileNamePath)
            logging.debug("      {0} FRAME was saved".format(frameFileNamePath))

            # ---

            # Create the path for CAPTURE if it dees not exist
            Path(capturePath).mkdir(parents=True, exist_ok=True)

            # Save CAPTURE
            img.save(captureFileNamePath)
            logging.debug("      {0} CAPTURE was saved".format(frameFileNamePath))

            # ---

            return output_json( {'result': 'OK'}, EP.CODE_OK)

        else:

            logging.error( "      !!! No {0} was saved as there was NO image sent) !!!".format(frameFileNamePath))
            return output_json( {'result': 'ERROR'}, EP.CODE_BAD_REQUEST)



