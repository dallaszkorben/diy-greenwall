import os
import requests
import logging
from datetime import datetime

class Cam:

    def __init__(self, web_gadget):

        self.webGadget = web_gadget

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
