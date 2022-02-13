import json

from flask import Flask
from flask import jsonify
from flask import session
from flask_classful import FlaskView, route, request

from restserver.representations import output_json

from config.permanent_data import getPermanentData
from config.permanent_data import setPermanentData
from config.config import getConfig

from exceptions.invalid_api_usage import InvalidAPIUsage

from restserver.endpoints.ep_lamp_register import EPLampRegister

from restserver.endpoints.ep import EP


# -----------------------------------
#
# POST Contorl the lamp
#
# curl  --header "Content-Type: application/json" --request POST http://localhost:5000/lamp/register/dateString/2021.12.03T11:34/lampId/5
# curl  --header "Content-Type: application/json" --request POST --data '{"lampId": "5", "dateString":"2021.12.03T11:34"}' http://localhost:5000/lamp/register
#
# -----------------------------------
#
# POST http://localhost:5000/lamp/register
class LampView(FlaskView):
    representations = {'application/json': output_json}
    inspect_args = False

    def __init__(self, web_gadget):

        self.web_gadget = web_gadget

        self.epLampRegister = EPLampRegister(web_gadget)

    #
    # GET http://localhost:5000/lamp/register
    #
    def index(self):
        return {}

# ===

    #
    # Register Lamp with payload
    #
    # curl  --header "Content-Type: application/json" --request POST --data '{"lampId": "5","dateString":"2021.12.03T11:34"}' http://localhost:5000/lamp/register
    #
    # POST http://localhost:5000/lamp/register
    #      body: {
    #        "dateString":"2021.12.03T11:34"
    #        "lampId": "5",
    #      }
    #
    #@route('/register', methods=['POST'])
    @route(EPLampRegister.PATH_PAR_PAYLOAD, methods=[EPLampRegister.METHOD])
    def setWithPayload(self):

        # WEB
        if request.form:
            json_data = request.form

        # CURL
        elif request.json:
            json_data = request.json

        else:
            return "Not valid request", EP.CODE_BAD_REQUEST

        out = self.epLampRegister.executeByPayload(json_data)
        return out

    #
    # Read the sensor - with parameters
    #
    # curl  --header "Content-Type: application/json" --request POST http://localhost:5000/lamp/register/dateString/2021.12.03T11:34/lampId/5
    #
    # POST http://localhost:5000/lamp/register/dateString/<dateString>'/lampId/5
    #
    #@route('/register/dateString/<dateString>'/lampId/<lampId>)
    @route(EPLampRegister.PATH_PAR_URL, methods=[EPLampRegister.METHOD])
    def setWithParameter(self, dateString, lampId):

        out = self.epLampRegister.executeByParameters(dateString=dateString, lampId=lampId)
        return out

