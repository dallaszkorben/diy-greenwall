import json

from flask import Flask
from flask import jsonify
from flask import session
from flask_classful import FlaskView, route, request

from greenwall.config.permanent_data import getPermanentData
from greenwall.config.permanent_data import setPermanentData
from greenwall.config.config import getConfig

from greenwall.exceptions.invalid_api_usage import InvalidAPIUsage

from greenwall.restserver.representations import output_json

from greenwall.restserver.endpoints.ep_pump_register import EPPumpRegister
from greenwall.restserver.endpoints.ep_pump_turn_on import EPPumpTurnOn
from greenwall.restserver.endpoints.ep_pump_turn_off import EPPumpTurnOff
from greenwall.restserver.endpoints.ep_pump_status import EPPumpStatus

from greenwall.restserver.endpoints.ep import EP


# -----------------------------------
#
# POST Contorl the pump
#
# curl  --header "Content-Type: application/json" --request POST http://localhost:5000/pump/register/dateString/2021.12.03T11:34/pumpId/5
# curl  --header "Content-Type: application/json" --request POST --data '{"pumpId": "5", "dateString":"2021.12.03T11:34"}' http://localhost:5000/pump/register

# curl  --header "Content-Type: application/json" --request POST http://localhost:5000/pump/turnOn/lengthInSec/10
# curl  --header "Content-Type: application/json" --request POST --data '{"lengthInSec": "10"}' http://localhost:5000/pump/turnOn


#
# curl  --header "Content-Type: application/json" --request GET http://localhost:5000/pump/status



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
        self.epPumpStatus = EPPumpStatus(web_gadget)
        self.epPumpTurnOn = EPPumpTurnOn(web_gadget)
        self.epPumpTurnOff = EPPumpTurnOff(web_gadget)


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
    def registerWithPayload(self):

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
    def registerWithParameter(self, dateString, pumpId):

        out = self.epPumpRegister.executeByParameters(dateString=dateString, pumpId=pumpId)
        return out



# ===

    #
    # Turn ON All Pump with payload
    #
    # curl  --header "Content-Type: application/json" --request POST --data '{"lengthInSec": "10"}' http://localhost:5000/pump/turnOn
    #
    # POST http://localhost:5000/pump/turnOn
    #      body: {
    #        "lengthInSec": "10",
    #      }
    #
    #@route('/turnOn', methods=['POST'])
    @route(EPPumpTurnOn.PATH_PAR_PAYLOAD, methods=[EPPumpTurnOn.METHOD])
    def setTurnOnWithPayload(self):

        # WEB
        if request.form:
            json_data = request.form

        # CURL
        elif request.json:
            json_data = request.json

        else:
            return "Not valid request", EP.CODE_BAD_REQUEST

        out = self.epPumpTurnOn.executeByPayload(json_data)
        return out

    #
    # Turn ON All Pump - with parameters
    #
    # curl  --header "Content-Type: application/json" --request POST http://localhost:5000/pump/turnOn/lengthInSec/10
    #
    # POST http://localhost:5000/pump/turnOn/lengthInSec/<lengthInSec>
    #
    #@route('/turnOn/lengthInSec/<lengthInSec>)
    @route(EPPumpTurnOn.PATH_PAR_URL, methods=[EPPumpTurnOn.METHOD])
    def setTurnOnWithParameter(self, lengthInSec):

        out = self.epPumpTurnOn.executeByParameters(lengthInSec=lengthInSec)
        return out



# ===

    #
    # Turn OFF All Pump - with parameters
    #
    # curl  --header "Content-Type: application/json" --request POST http://localhost:5000/pump/turnOff
    #
    # POST http://localhost:5000/pump/turnOff
    #
    #@route('/turnOff')
    @route(EPPumpTurnOff.PATH_PAR_URL, methods=[EPPumpTurnOff.METHOD])
    def setTurnOffWithParameter(self):

        out = self.epPumpTurnOff.executeByParameters()
        return out






# ===

    #
    # Get status of the Pump with parameters
    #
    # curl  --header "Content-Type: application/json" --request GET http://localhost:5000/pump/status
    #
    # GET http://localhost:5000/pump/status
    #
    #@route('/status', methods=['GET'])
    @route(EPPumpStatus.PATH_PAR_URL, methods=[EPPumpStatus.METHOD])
    def getStatusWithParameter(self):

        out = self.epPumpStatus.executeByParameters()
        return out






