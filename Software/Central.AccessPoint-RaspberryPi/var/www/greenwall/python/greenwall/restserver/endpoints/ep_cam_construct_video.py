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

class EPCamConstructVideo(EP):

    ID = 'cam_construct_video'
    URL = '/cam/construct/video'

    PATH_PAR_PAYLOAD = '/construct/video'
    PATH_PAR_URL = '/construct/video/camId/<camId>/startDate/<startDate>/endDate/<endDate>/fps/<fps>'

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
        ret['id'] = EPCamConstructVideo.ID
        ret['method'] = EPCamConstructVideo.METHOD
        ret['path-parameter-in-payload'] = EPCamConstructVideo.PATH_PAR_PAYLOAD
        ret['path-parameter-in-url'] = EPCamConstructVideo.PATH_PAR_URL

        ret['parameters'] = [{},{},{},{}]

        ret['parameters'][0]['attribute'] = EPCamConstructVideo.ATTR_CAM_ID
        ret['parameters'][0]['type'] = 'string'
        ret['parameters'][0]['value'] = 255

        ret['parameters'][1]['attribute'] = EPCamConstructVideo.ATTR_START_DATE
        ret['parameters'][1]['type'] = 'string'
        ret['parameters'][1]['value'] = 255

        ret['parameters'][2]['attribute'] = EPCamConstructVideo.ATTR_END_DATE
        ret['parameters'][2]['type'] = 'string'
        ret['parameters'][2]['value'] = 255

        ret['parameters'][3]['attribute'] = EPCamConstructVideo.ATTR_FPS
        ret['parameters'][3]['type'] = 'string'
        ret['parameters'][3]['value'] = 255

        return ret

    def executeByParameters(self, camId, startDate, endDate, fps) -> dict:
        payload = {}
        payload[EPCamFrameVideo.ATTR_CAM_ID] = camId
        payload[EPCamFrameVideo.ATTR_START_DATE] = startDate
        payload[EPCamFrameVideo.ATTR_END_DATE] = endDate
        payload[EPCamFrameVideo.ATTR_FPS] = fps

        with self.lockExecuteSave:
            return self.executeByPayload(payload)

    def executeByPayload(self, payload) -> dict:

        camId = payload[EPCamConstructVideo.ATTR_CAM_ID]
        startDate = payload[EPCamConstructVideo.ATTR_START_DATE]
        endDate = payload[EPCamConstructVideo.ATTR_END_DATE]
        fps = payload[EPCamConstructVideo.ATTR_FPS]

        logging.debug( "   REST request was received: {0} {1} ('{2}': {3}, '{4}': {5}, '{6}': {7}, '{8}': {9})".format(
                EPCamConstructVideo.METHOD, EPCamConstructVideo.URL,
                EPCamConstructVideo.ATTR_CAM_ID, camId,
                EPCamConstructVideo.ATTR_START_DATE, startDate,
                EPCamConstructVideo.ATTR_END_DATE, endDate,
                EPCamConstructVideo.ATTR_FPS, fps ))

        x = threading.Thread(target=self.constructVideo, args=(camId, startDate, endDate, fps))
        x.start()

        return output_json( {'result': 'OK'}, EP.CODE_OK)

# ---

    def constructVideo(self, camId, startDate, endDate, fps):
        """
            Construct webm video for the web by the parameters
        """

        logging.debug("!!! ConstructVideo Thread has started !!!")

        absoluteCamFrameFolder = self.web_gadget.absoluteCamFrameFolder
        absoluteCamVideoFolder = self.web_gadget.absoluteCamVideoFolder
        framePath = os.path.join(absoluteCamFrameFolder, camId)
        videoPath = os.path.join(absoluteCamVideoFolder, camId)
        videoFile = "video.webm"
        videoFilePath = os.path.join(videoPath, videoFile)

        # Create the path if it dees not exist
        Path(videoPath).mkdir(parents=True, exist_ok=True)

        fps=int(fps)

        logging.debug("   ConstructVideo - Video file: " + videoFilePath)

        out=cv2.VideoWriter(videoFilePath, cv2.VideoWriter.fourcc(*'VP80'), fps, (800,600))
        logging.debug("   ConstructVideo - Try to save video")
        try:
            for filename in natsorted(os.listdir(framePath)):

                ext = os.path.splitext(filename)[-1].lower()
                if ext=='.jpg' and startDate <= filename <= endDate:

                    logging.debug("   ConstructVideo - !!! " + filename + " !!!")

                    img=cv2.imread(os.path.join(framePath, filename))
                    out.write(img)

        finally:
            out.release()

        logging.debug("   ConstructVideo - {0} video was saved".format(videoFile))
        logging.debug("!!! ConstructVideo Thread Stops !!!")




