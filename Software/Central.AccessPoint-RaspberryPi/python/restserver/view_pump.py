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

from restserver.endpoints.ep_pump_register import EPPumpRegister

from restserver.endpoints.ep import EP


# -----------------------------------
#
# POST Contorl the pump
#
# curl  --header "Content-Type: application/json" --request POST http://localhost:5000/pump/register/dateString/2021.12.03T11:34/pumpId/5
# curl  --header "Content-Type: application/json" --request POST --data '{"pumpId": "5", "dateString":"2021.12.03T11:34"}' http://localhost:5000/pump/register
#
# -----------------------------------
#
# POST http://localhost:5000/pump/register
class PumpView(FlaskView):
    representations = {'application/json': output_json}
    inspect_args = False

    def __init__(self, web_gadget):

        self.web_gadget = web_gadget

        self.epPumpRegister = EPPumpRegister(web_gadget)

    #
    # GET http://localhost:5000/pump/register
    #
    def index(self):
        return {}

# ===

    #
    # Register Pump with payload
    #
    # curl  --header "Content-Type: application/json" --request POST --data '{"pumpId": "5","dateString":"2021.12.03T11:34"}' http://localhost:5000/pump/register
    #
    # POST http://localhost:5000/pump/register
    #      body: {
    #        "dateString":"2021.12.03T11:34"
    #        "pumpId": "5",
    #      }
    #
    #@route('/register', methods=['POST'])
    @route(EPPumpRegister.PATH_PAR_PAYLOAD, methods=[EPPumpRegister.METHOD])
    def setWithPayload(self):

        # WEB
        if request.form:
            json_data = request.form

        # CURL
        elif request.json:
            json_data = request.json

        else:
            return "Not valid request", EP.CODE_BAD_REQUEST

        out = self.epPumpRegister.executeByPayload(json_data)
        return out

    #
    # Read the sensor - with parameters
    #
    # curl  --header "Content-Type: application/json" --request POST http://localhost:5000/pump/register/dateString/2021.12.03T11:34/pumpId/5
    #
    # POST http://localhost:5000/pump/register/dateString/<dateString>'/pumpId/5
    #
    #@route('/register/dateString/<dateString>'/pumpId/<pumpId>)
    @route(EPPumpRegister.PATH_PAR_URL, methods=[EPPumpRegister.METHOD])
    def setWithParameter(self, dateString, pumpId):

        out = self.epPumpRegister.executeByParameters(dateString=dateString, pumpId=pumpId)
        return out
