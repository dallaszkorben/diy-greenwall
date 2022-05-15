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

from restserver.endpoints.ep_lamp_switch import EPLampSwitch
from restserver.endpoints.ep_lamp_register import EPLampRegister
from restserver.endpoints.ep_lamp_status import EPLampStatus


from restserver.endpoints.ep import EP


# -----------------------------------
#
# POST Control the Lamp
#
# curl  --header "Content-Type: application/json" --request POST http://localhost:5000/lamp/register/dateString/2021.12.03T11:34/lampId/5
# curl  --header "Content-Type: application/json" --request POST --data '{"lampId": "5", "dateString":"2021.12.03T11:34"}' http://localhost:5000/lamp/register
#
# curl  --header "Content-Type: application/json" --request POST http://localhost:5000/lamp/switch/status/on/lengthInSec/10
# curl  --header "Content-Type: application/json" --request POST --data '{"status": "on", "lengthInSec": "10"}' http://localhost:5000/lamp/switch
#
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
        self.epLampSwitch = EPLampSwitch(web_gadget)
        self.epLampStatus = EPLampStatus(web_gadget)

    #
    # GET http://localhost:5000/lamp
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
    def setRegisterWithPayload(self):

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
    # Register Lamp  with parameters
    #
    # curl  --header "Content-Type: application/json" --request POST http://localhost:5000/lamp/register/dateString/2021.12.03T11:34/lampId/5
    #
    # POST http://localhost:5000/lamp/register/dateString/<dateString>'/lampId/5
    #
    #@route('/register/dateString/<dateString>'/lampId/<lampId>)
    @route(EPLampRegister.PATH_PAR_URL, methods=[EPLampRegister.METHOD])
    def setRegisterWithParameter(self, dateString, lampId):

        out = self.epLampRegister.executeByParameters(dateString=dateString, lampId=lampId)
        return out



# ===

    #
    # Switch All Lamp with payload
    #
    # curl  --header "Content-Type: application/json" --request POST --data '{"status": "on", "lengthInSec": "10"}' http://localhost:5000/lamp/switch
    #
    # POST http://localhost:5000/lamp/switch
    #      body: {
    #        "status": "on", #on/off
    #        "lengthInSec": "10",
    #      }
    #
    #@route('/switch', methods=['POST'])
    @route(EPLampSwitch.PATH_PAR_PAYLOAD, methods=[EPLampSwitch.METHOD])
    def setSwitchWithPayload(self):

        # WEB
        if request.form:
            json_data = request.form

        # CURL
        elif request.json:
            json_data = request.json

        else:
            return "Not valid request", EP.CODE_BAD_REQUEST

        out = self.epLampSwitch.executeByPayload(json_data)
        return out

    #
    # Switch All Lamp - with parameters
    #
    # curl  --header "Content-Type: application/json" --request POST http://localhost:5000/lamp/switch/status/on/lengthInSec/10
    #
    # POST http://localhost:5000/lamp/switch/status/<status>/lengthInSec/<lengthInSec>
    #
    #@route('/switch/status/<status>'/lengthInSec/<lengthInSec>)
    @route(EPLampSwitch.PATH_PAR_URL, methods=[EPLampSwitch.METHOD])
    def setSwitchWithParameter(self, status, lengthInSec):

        out = self.epLampSwitch.executeByParameters(status=status, lengthInSec=lengthInSec)
        return out





# ===

    #
    # Get status of the Lamp with parameters
    #
    # curl  --header "Content-Type: application/json" --request GET http://localhost:5000/lamp/status
    #
    # GET http://localhost:5000/lamp/status
    #
    #@route('/status', methods=['GET'])
    @route(EPLampStatus.PATH_PAR_URL, methods=[EPLampStatus.METHOD])
    def getStatusWithParameter(self):

        out = self.epLampStatus.executeByParameters()
        return out















