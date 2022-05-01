import json

#from flask_api import status

from flask import Flask
from flask import jsonify
from flask import session
from flask_classful import FlaskView, route, request

from restserver.representations import output_json

from config.permanent_data import getPermanentData
from config.permanent_data import setPermanentData
from config.config import getConfig

from exceptions.invalid_api_usage import InvalidAPIUsage

from restserver.endpoints.ep_cam_stream_register import EPCamStreamRegister
from restserver.endpoints.ep_cam_add import EPCamAdd

from restserver.endpoints.ep import EP

from PIL import Image

# -----------------------------------
#
# POST Contorl the sensor of the light
#
# curl  --header "Content-Type: img/jpeg" --request POST --data '...' http://localhost:5000/cam/add/camId/5
#
# -----------------------------------
#
# POST http://localhost:5000/cam
class CamView(FlaskView):
    representations = {'application/json': output_json}
    inspect_args = False

    def __init__(self, web_gadget):

        self.web_gadget = web_gadget

        self.epCamStreamRegister = EPCamStreamRegister(web_gadget)
        self.epCamAdd = EPCamAdd(web_gadget)


    #
    # GET http://localhost:5000/sensor/
    #
    def index(self):
        return {}




# ===

    #
    # Register Cam Stream with payload
    #
    # curl  --header "Content-Type: application/json" --request POST --data '{"id": "5","url":"http://192.168.50.123:81/stream"}' http://localhost:5000/cam/stream/register
    #
    # POST http://localhost:5000/cam/stream/register
    #      body: {
    #        "id":"5"
    #        "url": "http://192.168.50.123:81/stream",
    #      }
    #
    #@route('/stream/register', methods=['POST'])
    @route(EPCamStreamRegister.PATH_PAR_PAYLOAD, methods=[EPCamStreamRegister.METHOD])
    def setWithPayload(self):

        # WEB
        if request.form:
            json_data = request.form

        # CURL
        elif request.json:
            json_data = request.json

        else:
            return "Not valid request", EP.CODE_BAD_REQUEST

        out = self.epCamStreamRegister.executeByPayload(json_data)
        return out








# ===

    #
    # Set the sensor with payload
    #
    # curl  --header "Content-Type: img/jpeg" --request POST --data '...' http://localhost:5000/cam/add/camId/5/timestamp/2022.11.23T11:22:12
    #
    #@route('/add/camId/<camId>/timestamp/<timestamp>', methods=['POST'])
#    @route(EPCamAdd.PATH_PAR_PAYLOAD, methods=[EPCamAdd.METHOD])
#    def setWithPayload(self):
#
#        # WEB
#        if request.form:
#            json_data = request.form
#
#        # CURL
#        elif request.json:
#            json_data = request.json
#
#        else:
#            return "Not valid request", EP.CODE_BAD_REQUEST
#
#        out = self.epCamAdd.executeByPayload(json_data)

#        return out



    #
    # Read the sensor - with parameters
    #
    # curl  --header "Content-Type: img/jpeg" --request POST --data '...' http://localhost:5000/cam/add/camId/5/timestamp/2022.11.23T11:22:12
    #
    #@route('/add/camId/<camId>/timestamp/<timestamp>', methods=['POST'])
    @route(EPCamAdd.PATH_PAR_URL, methods=[EPCamAdd.METHOD])
    def addCamCaptureWithParameter(self, camId, timestamp):

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


        if "imageFile" in request.files:
            image = request.files["imageFile"];
#            if image:
#            img = Image.open(image)
#            img.save("output.jpg")

            print("file was received")


        else:
            image = None
            print("!!! No file was received")

        out = self.epCamAdd.executeByParameters(camId=camId, timestamp=timestamp, image=image)
        return out






