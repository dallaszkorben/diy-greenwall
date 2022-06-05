import os
import requests
import logging
from datetime import datetime

class Cam:

    def __init__(self, web_gadget):

        self.webGadget = web_gadget

    # TODO Have to fix the selection of camera. Now selects the first 
    def getCapture(self, camId):

        webRootPath = self.webGadget.webRootPath
        webCamCaptureFolder = self.webGadget.webCamCaptureFolder
        webCamCaptureFile = self.webGadget.webCamCaptureFile.format(camId)
        fileName = os.path.join(webRootPath, webCamCaptureFolder, webCamCaptureFile)

        for key, value in self.webGadget.registerCam.camDict.items():

            address = value["captureUrl"]
            data = {}

            try:

                #with requests.get(address, timeout=20, stream=True) as r:
                #    logging.debug("Downloaded Frame's StatusCode: {0}".format(x.status_code))
                #
                #    r.raise_for_status()
                #    with open( fileName 'wb') as f:
                #        for chunk in r.iter_content(chunk_size=8192):
                #            f.write(chunk)

                logging.debug("cam.py Sends request: GET {0}".format(address))
                response = requests.get(address, timeout=20)
                logging.debug("Downloaded Frame's StatusCode: {0}".format(response.status_code))

                open(fileName, "wb").write(response.content)

            except Exception as e:

                logging.error("Exception while fetch the frame from the camera: {0}.".format(e))

        return fileName
                
    def getCamStatus(self):

        addresses = []

        # TODO later I should handle more lamps. Now works only one
        for key, value in self.webGadget.registerLamp.lampDict.items():

            actDateTime = datetime.now().astimezone()
            actTimeStamp = datetime.timestamp(actDateTime)
            regTimeStamp = value["timeStamp"]
            diffSec = (actTimeStamp - regTimeStamp)

            # if less than 120 seconds was re-registering
            if diffSec < 120:
                addresses.append("http://{url}/lamp/status".format(url=value["ip"]))

        try:

            address = addresses[0]

            x = requests.get(address, timeout=20)
            response = x.json()

            logging.debug("StatusCode: {0}".format(x.status_code))

            if x.status_code == 200:
                logging.debug("Response: {0}".format(x.text))
                return response.get('status')
            else:
                logging.debug("Response: Failed. Status is n/a")
                return 'n/a'


        # NewConnectionError
        # ConnectTimeoutError
        except Exception as e:

            if len(addresses) == 0:
                logging.debug("No lamp registered.")
            else:
                logging.error("Exception: {0}. Status is n/a".format(e))
            return 'n/a'
