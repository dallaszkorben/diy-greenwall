import json

#from flask_api import status

from flask import Flask
from flask import jsonify
from flask import session
from flask_classful import FlaskView, route, request

from greenwall.restserver.representations import output_json

from greenwall.config.permanent_data import getPermanentData
from greenwall.config.permanent_data import setPermanentData
from greenwall.config.config import getConfig

from greenwall.restserver.endpoints.ep_cam_register import EPCamRegister
from greenwall.restserver.endpoints.ep_cam_frame_save import EPCamFrameSave
from greenwall.restserver.endpoints.ep_cam_capture_url import EPCamCaptureUrl
from greenwall.restserver.endpoints.ep_cam_capturelist import EPCamCaptureList

from greenwall.restserver.endpoints.ep import EP

from greenwall.exceptions.invalid_api_usage import InvalidAPIUsage


from PIL import Image

# -----------------------------------
#
#
# -----------------------------------
#
# POST http://localhost:5000/cam
class CamView(FlaskView):
    representations = {'application/json': output_json}
    inspect_args = False

    def __init__(self, web_gadget):

        self.web_gadget = web_gadget

        self.epCamRegister = EPCamRegister(web_gadget)
        self.epCamFrameSave = EPCamFrameSave(web_gadget)
        self.epCamCaptureUrl = EPCamCaptureUrl(web_gadget)
        self.epCamCaptureList = EPCamCaptureList(web_gadget)


    #
    # GET http://localhost:5000/sensor/
    #
    def index(self):
        return {}




# === POST /stream ===

    #
    # Register Cam Stream with payload
    #
    # curl  --header "Content-Type: application/json" --request POST --data '{"camId": "5","streamUrl":"http://192.168.50.123:81/stream", "captureUrl": "http://192.168.50.123:80/capture" }' http://localhost:5000/cam/register
    #
    # POST http://localhost:5000/cam/stream/register
    #      body: {
    #        "camId":"5"
    #        "streamUrl": "http://192.168.50.123:81/stream",
    #        "captureUrl": "http://192.168.50.123:80/capture",
    #      }
    #
    #@route('/register', methods=['POST'])
    @route(EPCamRegister.PATH_PAR_PAYLOAD, methods=[EPCamRegister.METHOD])
    def registerCamWithPayload(self):

        # WEB
        if request.form:
            json_data = request.form

        # CURL
        elif request.json:
            json_data = request.json

        else:
            return "Not valid request", EP.CODE_BAD_REQUEST

        out = self.epCamRegister.executeByPayload(json_data)
        return out



# === POST /cam/frame/save/ ===

    #
    # Save frame - with parameters
    #
    # curl  --header "Content-Type: img/jpeg" --request POST --data '...' http://localhost:5000/cam/frame/save/camId/5/timestamp/2022.11.23T11:22:12
    #
    #@route('/frame/save/camId/<camId>/timestamp/<timestamp>', methods=['POST'])
    @route(EPCamFrameSave.PATH_PAR_URL, methods=[EPCamFrameSave.METHOD])
    def saveCamFrameWithParameter(self, camId, timestamp):

        from pprint import pprint
        print("!!! Request !!!")

        pprint(request.headers)
        pprint(request.data)
        pprint(request.args)
        pprint(request.form)
        pprint(request.endpoint)
        pprint(request.method)
        pprint(request.remote_addr)
        pprint(request.json)
        pprint(request.files)


        if "frameFile" in request.files:
            image = request.files["frameFile"];
#            if image:
#            img = Image.open(image)
#            img.save("output.jpg")

            print("file was received")

        else:
            image = None
            print("!!! No file was received")

        out = self.epCamFrameSave.executeByParameters(camId=camId, image=image, timestamp=timestamp)
        return out


# === GET /cam/capture/url/camId/5 ===

    #
    # Take photo and give back the saved file's url - with parameters
    #
    # curl  --header "Content-Type: img/jpeg" --request GET --data  http://localhost:5000/cam/capture/url/camId/5
    #
    #@route('/capture/url', methods=['GET'])
    @route(EPCamCaptureUrl.PATH_PAR_URL, methods=[EPCamCaptureUrl.METHOD])
    def takePhotoGetUrlWithParameter(self, camId):

        out = self.epCamCaptureUrl.executeByParameters(camId=camId)
        return out



# === GET /cam/captureList ===

    #
    # Get the list of the URLs of Capture Cameras - with payload
    #
    # curl  --header "Content-Type: application/json" --request GET http://localhost:5000/cam/captureList
    #
    # GET http://localhost:5000/cam/captureList
    #
    #@route('/captureList', methods=['GET'])
    @route(EPCamCaptureList.PATH_PAR_PAYLOAD, methods=[EPCamCaptureList.METHOD])
    def getListOfCaptureCamUrlList(self):

        out = self.epCamCaptureList.executeByParameters()
        return out


