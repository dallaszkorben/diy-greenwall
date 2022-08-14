import os
import requests
import logging
from pathlib import Path
from datetime import datetime
from threading import Lock
from threading import Thread

import cv2
import os
from natsort import natsorted

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 

class Cam:

    def __init__(self, web_gadget):

        self.webGadget = web_gadget

        self.lockVideoConstruct = Lock()
        self.statusVideoConstruct = {}
        self.setProgressVideoConstruct(False)

    def getCapture(self, camId):
        """
        Take a picture of the camera, save it into the file system and return the web path to the file
        It is called from the web page
        """

        absoluteRootPath = self.webGadget.absoluteRootPath
        webCamCaptureFolder = self.webGadget.webCamCaptureFolder
        webCamCaptureFile = self.webGadget.webCamCaptureFile.format(camId)
        webRootPath = self.webGadget.webRootPath

        webFilePath = os.path.join(webRootPath, webCamCaptureFolder, webCamCaptureFile)
        absoluteFilePath = os.path.join(absoluteRootPath, webCamCaptureFolder, webCamCaptureFile)

        # if the camId is registered
        value = self.webGadget.registerCam.getCamDictValue(camId)
        if value:

            address = value["captureUrl"]
            data = {}

            try:
                logging.debug("cam.py Sends request: GET {0}".format(address))

                # Send request to take photo
                response = requests.get(address, timeout=20)

                logging.debug("Downloaded Frame's StatusCode: {0}".format(response.status_code))

                # save the captured photo
                open(absoluteFilePath, "wb").write(response.content)

            except Exception as e:
                logging.error("Exception while fetch the frame 'GET {0}' from the camera: {1}.".format(address, e))

        return webFilePath

    def videoConstruct(self, camId, startDate, endDate, fps):
        """
            Construct webm video for the web by the parameters and place it into the folder configure in the config.ini:

            [absolute]
            cam-video-folder

            for example: /var/www/greenwall/cam-video/{camId}

            The process takes lot of time to run so this method is called as a Thread
            The process is a very resource-intensive task consequently only 1 thread is allowed to run at the time
        """

        # If I can not lock - an other request already locked
        if not self.lockVideoConstruct.acquire(False):

            logging.error("!!! New request arrived to constructVideo ({0}) while the previous request is still running !!!".format(camId))

            # then will be not construct video
            return False

        else:

            x = Thread(target=self.threadVideoConstruct, args=(camId, startDate, endDate, fps))
            x.start()
            return True


    def threadVideoConstruct(self, camId, startDate, endDate, fps):

        self.setProgressVideoConstruct(True, camId, 0)

        logging.debug("!!! constructVideo ({0}) Thread has started !!!".format(camId))

        absoluteCamFrameFolder = self.webGadget.absoluteCamFrameFolder
        absoluteCamVideoFolder = self.webGadget.absoluteCamVideoFolder
        framePath = os.path.join(absoluteCamFrameFolder, camId)
        videoPath = os.path.join(absoluteCamVideoFolder, camId)
        videoFile = "video.webm"
        videoFilePath = os.path.join(videoPath, videoFile)

        # Create the path if it dees not exist
        Path(videoPath).mkdir(parents=True, exist_ok=True)

        fps=int(fps)

        logging.debug("   constructVideo ({0}) - Video file: ({1})".format(camId, videoFilePath))

        out=cv2.VideoWriter(videoFilePath, cv2.VideoWriter.fourcc(*'VP80'), fps, (800,600))
        logging.debug("   constructVideo ({0}) - Try to save video".format(camId))

        # count the number of files for video
        numberOfFiles = 0
        for filename in natsorted(os.listdir(framePath)):
                ext = os.path.splitext(filename)[-1].lower()
                if ext=='.jpg' and startDate <= filename <= endDate:
                    numberOfFiles += 1

        indexOfFile = 0
        try:
            for filename in natsorted(os.listdir(framePath)):

                ext = os.path.splitext(filename)[-1].lower()
                if ext=='.jpg' and startDate <= filename <= endDate:
                    indexOfFile += 1

                    logging.debug("   constructVideo ({0}) - !!! {1} !!!".format(camId, filename))

                    progress = indexOfFile / numberOfFiles
                    self.setProgressVideoConstruct(True, camId, progress)

                    logging.error("            {0}% progress".format(progress))

                    img=cv2.imread(os.path.join(framePath, filename))
                    out.write(img)

        finally:
            out.release()

        logging.debug("   ConstructVideo ({0}) - {1} video was saved".format(camId, videoFile))
        logging.debug("!!! constructVideo ({0}) Thread Stops !!!".format(camId))

        self.setProgressVideoConstruct(False)
        self.lockVideoConstruct.release()

    def setProgressVideoConstruct(self, inProgress, camId=None, progress=None):
        if inProgress:
            self.statusVideoConstruct['inProgress'] = True
            self.statusVideoConstruct['camId'] = camId
            self.statusVideoConstruct['progress'] = progress
        else:
            self.statusVideoConstruct['inProgress'] = False
            self.statusVideoConstruct['camId'] = None
            self.statusVideoConstruct['progress'] = None

    def getProgressVideoConstruct(self):
        return self.statusVideoConstruct


    def getFrameFiles(self, camId):
        """
            Gives back the frame file list of a camId
        """

        fileList = []

        logging.debug("Start to collect of the Frame files of {0} Cam".format(camId))

        absoluteCamFrameFolder = self.webGadget.absoluteCamFrameFolder
        framePath = os.path.join(absoluteCamFrameFolder, camId)
        for filename in natsorted(os.listdir(framePath)):

            ext = os.path.splitext(filename)[-1].lower()
            if ext=='.jpg': #and startDate <= filename <= endDate:
                fileList.append(filename)

        logging.debug("Stopped to collect of the Frame files of {0} Cam".format(camId))

        return {'fileList': fileList}

#    def getCamStatus(self):
#
#        addresses = []
#
#        # TODO later I should handle more lamps. Now works only one
#        for key, value in self.webGadget.registerLamp.lampDict.items():
#
#            actDateTime = datetime.now().astimezone()
#            actTimeStamp = datetime.timestamp(actDateTime)
#            regTimeStamp = value["timeStamp"]
#            diffSec = (actTimeStamp - regTimeStamp)
#
#            # if less than 120 seconds was re-registering
#            if diffSec < 120:
#                addresses.append("http://{url}/lamp/status".format(url=value["ip"]))
#
#        try:
#
#            address = addresses[0]
#
#            x = requests.get(address, timeout=20)
#            response = x.json()
#
#            logging.debug("StatusCode: {0}".format(x.status_code))
#
#            if x.status_code == 200:
#                logging.debug("Response: {0}".format(x.text))
#                return response.get('status')
#            else:
#                logging.debug("Response: Failed. Status is n/a")
#                return 'n/a'
#
#
#        # NewConnectionError
#        # ConnectTimeoutError
#        except Exception as e:
#
#            if len(addresses) == 0:
#                logging.debug("No lamp registered.")
#            else:
#                logging.error("Exception: {0}. Status is n/a".format(e))
#            return 'n/a'
