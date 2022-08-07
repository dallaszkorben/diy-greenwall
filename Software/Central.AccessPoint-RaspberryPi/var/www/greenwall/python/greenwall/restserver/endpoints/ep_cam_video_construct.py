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

class EPCamVideoConstruct(EP):

    ID = 'cam_video_construct'
    URL = '/cam/video/construct'

    PATH_PAR_PAYLOAD = '/video/construct'
    PATH_PAR_URL = '/video/construct/camId/<camId>/startDate/<startDate>/endDate/<endDate>/fps/<fps>'

    METHOD = 'POST'

    ATTR_CAM_ID = 'camId'
    ATTR_START_DATE = 'startDate'
    ATTR_END_DATE = 'endDate'
    ATTR_FPS = 'fps'

    def __init__(self, web_gadget):
        self.web_gadget = web_gadget

        self.lockExecuteSave = Lock()

    @staticmethod
    def getRequestDescriptionWithPayloadParameters():

        ret = {}
        ret['id'] = EPCamVideoConstruct.ID
        ret['method'] = EPCamVideoConstruct.METHOD
        ret['path-parameter-in-payload'] = EPCamVideoConstruct.PATH_PAR_PAYLOAD
        ret['path-parameter-in-url'] = EPCamVideoConstruct.PATH_PAR_URL

        ret['parameters'] = [{},{},{},{}]

        ret['parameters'][0]['attribute'] = EPCamVideoConstruct.ATTR_CAM_ID
        ret['parameters'][0]['type'] = 'string'
        ret['parameters'][0]['value'] = 255

        ret['parameters'][1]['attribute'] = EPCamVideoConstruct.ATTR_START_DATE
        ret['parameters'][1]['type'] = 'string'
        ret['parameters'][1]['value'] = 255

        ret['parameters'][2]['attribute'] = EPCamVideoConstruct.ATTR_END_DATE
        ret['parameters'][2]['type'] = 'string'
        ret['parameters'][2]['value'] = 255

        ret['parameters'][3]['attribute'] = EPCamVideoConstruct.ATTR_FPS
        ret['parameters'][3]['type'] = 'string'
        ret['parameters'][3]['value'] = 255

        return ret

    def executeByParameters(self, camId, startDate, endDate, fps) -> dict:
        payload = {}
        payload[EPCamVideoConstruct.ATTR_CAM_ID] = camId
        payload[EPCamVideoConstruct.ATTR_START_DATE] = startDate
        payload[EPCamVideoConstruct.ATTR_END_DATE] = endDate
        payload[EPCamVideoConstruct.ATTR_FPS] = fps

        with self.lockExecuteSave:
            return self.executeByPayload(payload)

    def executeByPayload(self, payload) -> dict:

        camId = payload[EPCamVideoConstruct.ATTR_CAM_ID]
        startDate = payload[EPCamVideoConstruct.ATTR_START_DATE]
        endDate = payload[EPCamVideoConstruct.ATTR_END_DATE]
        fps = payload[EPCamVideoConstruct.ATTR_FPS]

        logging.debug( "   REST request was received: {0} {1} ('{2}': {3}, '{4}': {5}, '{6}': {7}, '{8}': {9})".format(
                EPCamVideoConstruct.METHOD, EPCamVideoConstruct.URL,
                EPCamVideoConstruct.ATTR_CAM_ID, camId,
                EPCamVideoConstruct.ATTR_START_DATE, startDate,
                EPCamVideoConstruct.ATTR_END_DATE, endDate,
                EPCamVideoConstruct.ATTR_FPS, fps ))

        result = self.web_gadget.cam.videoConstruct(camId, startDate, endDate, fps)

        return output_json( {'result': 'OK' }, EP.CODE_OK) if result else output_json( {'result': 'ERROR' }, EP.CODE_BAD_REQUEST)

#        x = threading.Thread(target=self.web_gadget.cam.constructVideo, args=(camId, startDate, endDate, fps))
#        x = threading.Thread(target=self.constructVideo, args=(camId, startDate, endDate, fps))
#        x.start()


# ---

#    def constructVideo(self, camId, startDate, endDate, fps):
#        """
#            Construct webm video for the web by the parameters
#
#            That is a very resource-intensive task consequently only 1 thread is allowed to run at the time
#        """
#
#        logging.debug("!!! constructVideo ({0}) Thread has started !!!".format(camId))
#
#        absoluteCamFrameFolder = self.web_gadget.absoluteCamFrameFolder
#        absoluteCamVideoFolder = self.web_gadget.absoluteCamVideoFolder
#        framePath = os.path.join(absoluteCamFrameFolder, camId)
#        videoPath = os.path.join(absoluteCamVideoFolder, camId)
#        videoFile = "video.webm"
#        videoFilePath = os.path.join(videoPath, videoFile)
#
#        # Create the path if it dees not exist
#        Path(videoPath).mkdir(parents=True, exist_ok=True)
#
#        fps=int(fps)
#
#        logging.debug("   constructVideo ({0}) - Video file: ({1})".format(camId, videoFilePath))
#
#        out=cv2.VideoWriter(videoFilePath, cv2.VideoWriter.fourcc(*'VP80'), fps, (800,600))
#        logging.debug("   constructVideo ({0}) - Try to save video".format(camId))
#        try:
#            for filename in natsorted(os.listdir(framePath)):
#
#                ext = os.path.splitext(filename)[-1].lower()
#                if ext=='.jpg' and startDate <= filename <= endDate:
#
#                    logging.debug("   constructVideo ({0}) - !!! {1} !!!".format(camId, filename))
#
#                    img=cv2.imread(os.path.join(framePath, filename))
#                    out.write(img)
#
#        finally:
#            out.release()
#
#        logging.debug("   ConstructVideo ({0}) - {1} video was saved".format(camId, videoFile))
#        logging.debug("!!! constructVideo ({0}) Thread Stops !!!".format(camId))


