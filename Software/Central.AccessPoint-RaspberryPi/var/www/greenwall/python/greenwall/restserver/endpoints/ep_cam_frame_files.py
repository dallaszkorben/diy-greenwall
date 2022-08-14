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

import os
from natsort import natsorted

class EPCamFrameFiles(EP):

    ID = 'cam_frame_files'
    URL = '/cam/frame/files'

    PATH_PAR_PAYLOAD = '/frame/files'
    PATH_PAR_URL = '/frame/files/camId/<camId>'

    METHOD = 'GET'

    ATTR_CAM_ID = 'camId'

    def __init__(self, web_gadget):
        self.web_gadget = web_gadget

    @staticmethod
    def getRequestDescriptionWithPayloadParameters():

        ret = {}
        ret['id'] = EPCamFrameFiles.ID
        ret['method'] = EPCamFrameFiles.METHOD
        ret['path-parameter-in-payload'] = EPCamFrameFiles.PATH_PAR_PAYLOAD
        ret['path-parameter-in-url'] = EPCamFrameFiles.PATH_PAR_URL

        ret['parameters'] = [{},{}]

        ret['parameters'][0]['attribute'] = EPCamFrameFiles.ATTR_CAM_ID
        ret['parameters'][0]['type'] = 'string'
        ret['parameters'][0]['value'] = 255

        return ret

    def executeByParameters(self, camId) -> dict:
        payload = {}
        payload[EPCamFrameFiles.ATTR_CAM_ID] = camId

        return self.executeByPayload(payload)

    def executeByPayload(self, payload) -> dict:

        camId = payload[EPCamFrameFiles.ATTR_CAM_ID]

        logging.debug( "   REST request was received: {0} {1} ('{2}': {3})".format(
                EPCamFrameFiles.METHOD, EPCamFrameFiles.URL,
                EPCamFrameFiles.ATTR_CAM_ID, camId ))

        ret = self.web_gadget.cam.getFrameFiles(camId)
        ret["result"] = "OK"
        return output_json( ret, EP.CODE_OK)



#    def getFrameFiles(self, camId):
#        """
#            Gives back the frame file list of a camId
#        """
#
#        logging.debug("Start to collect of the Frame files of {0} Cam".format(camId))
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


