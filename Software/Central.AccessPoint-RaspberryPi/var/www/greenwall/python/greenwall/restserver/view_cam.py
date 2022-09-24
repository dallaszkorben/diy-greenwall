import logging

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
from greenwall.restserver.endpoints.ep_cam_save_frame import EPCamSaveFrame
from greenwall.restserver.endpoints.ep_cam_capture_url import EPCamCaptureUrl
from greenwall.restserver.endpoints.ep_cam_capturelist import EPCamCaptureList
from greenwall.restserver.endpoints.ep_cam_video_construct import EPCamVideoConstruct
from greenwall.restserver.endpoints.ep_cam_video_status import EPCamVideoStatus
from greenwall.restserver.endpoints.ep_cam_frame_files import EPCamFrameFiles

from greenwall.restserver.endpoints.ep import EP

from greenwall.exceptions.invalid_api_usage import InvalidAPIUsage

#from PIL import Image

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
        self.epCamSaveFrame = EPCamSaveFrame(web_gadget)
        self.epCamVideoConstruct = EPCamVideoConstruct(web_gadget)
        self.epCamCaptureUrl = EPCamCaptureUrl(web_gadget)
        self.epCamCaptureList = EPCamCaptureList(web_gadget)
        self.epCamVideoStatus = EPCamVideoStatus(web_gadget)
        self.epCamFrameFiles = EPCamFrameFiles(web_gadget)

    #
    # GET http://localhost:5000/sensor/
    #
    def index(self):
        return {}


# === POST /register ===

    #
    # Register Cam with payload
    #
    # curl  --header "Content-Type: application/json" --request POST --data '{"camId": "5","streamUrl":"http://192.168.50.123:81/stream", "captureUrl": "http://192.168.50.123:80/capture" }' http://localhost:5000/cam/register
    #
    # POST http://localhost:5000/cam/register
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



# === POST /cam/save/frame/camId/{camId}/camRotate/{camRotate} ===


    #
    # Save frame - with parameters - called from the cam module
    #
    # curl  --header "Content-Type: multipart/form-data; boundary=XmyOwnBoundryX" --header "X-camRotate: 0" --request POST --data '...' http://localhost:5000/cam/save/frame/camId/5/camRotate/0
    #
    #@route('/save/frame/camId/<camId>/camRotate/<camRotate>', methods=['POST'])
    @route(EPCamSaveFrame.PATH_PAR_URL, methods=[EPCamSaveFrame.METHOD])
    def saveCamFrameWithParameter(self, camId, camRotate):

#        from pprint import pprint
#        print("!!! Request: !!!")
#        print(request)
#        print("---")
#        print(vars(request))
#        print()
#        print("!!! Headers: !!!")
#        if hasattr(request, 'headers'):
#            pprint(request.headers)
#        if hasattr(request, 'data'):
#            pprint(request.data)
#        if hasattr(request, 'args'):
#            pprint(request.args)
#        if hasattr(request, 'form'):
#            pprint(request.form)
#        if hasattr(request, 'endpoing'):
#            pprint(request.endpoint)
#        if hasattr(request, 'method'):
#            pprint(request.method)
#        if hasattr(request, 'remote_addr'):
#            pprint(request.remote_addr)
#        if hasattr(request, 'json'):
#            pprint(request.json)
#        if hasattr(request, 'files'):
#            pprint(request.files)
#        else:
#            print("NO file was sent")
#        print()

        logging.debug("POST cam/save/frame/ node was called from the cam module")

        image = None
        try:
            if hasattr(request, 'files') and "frameFile" in request.files:

                image = request.files["frameFile"];

                logging.debug("   POST cam/save/frame node RECEIVED the image file. Now the image process starts.")

        except:
            logging.error("   !!! POST cam/save/frame node DID NOT receive the image file !!!")

        #camRotate=request.headers.get('X-Camrotate')
        #if not camRotate:
        #    camRotate = "0"

        out = self.epCamSaveFrame.executeByParameters(camId=camId, camRotate=camRotate, image=image)
        return out


# === POST /cam/video/construct/ ===

    #
    # Save frame - with parameters
    #
    # curl  --header "Content-Type: img/jpeg" --request POST --data '{"camId": "5","startDate":"", "endDate": "", "fps": "15"}' http://localhost:5000/cam/video/construct/
    #
    # POST http://localhost:5000/cam/video/construct/
    #      body: {
    #        "camId":"5"
    #        "startDate": "2022.06.18T07:12",
    #        "endDate": "2022.06.19T19:21",
    #      }

    #@route('/video/construct', methods=['POST'])
    @route(EPCamVideoConstruct.PATH_PAR_PAYLOAD, methods=[EPCamVideoConstruct.METHOD])
    def camConstructVideoWithPayload(self):

        # WEB
        if request.form:
            json_data = request.form

        # CURL
        elif request.json:
            json_data = request.json

        else:
            return "Not valid request", EP.CODE_BAD_REQUEST

        out = self.epCamVideoConstruct.executeByPayload(json_data)
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



# === GET /cam/video/status ===

    #
    # Get the status of the VideoMake - with parameters
    #
    # curl  --header "Content-Type: application/json" --request GET --data  http://localhost:5000/cam/video/status
    #
    #@route('/capture/url', methods=['GET'])
    @route(EPCamVideoStatus.PATH_PAR_URL, methods=[EPCamVideoStatus.METHOD])
    def getCamVideoStatusWithParameter(self):

        out = self.epCamVideoStatus.executeByParameters()
        return out


# === GET /cam/frame/files ===

    #
    # Get the file list of the frames of a camId
    #
    # curl  --header "Content-Type: application/json" --request GET --data  http://localhost:5000/cam/frame/files/camId/5
    #
    #@route('/frame/files/camId/{camId|', methods=['GET'])
    @route(EPCamFrameFiles.PATH_PAR_URL, methods=[EPCamFrameFiles.METHOD])
    def getCamFrameListWithParameter(self, camId):

        out = self.epCamFrameFiles.executeByParameters(camId=camId)
        return out


