import json

#from flask_api import status

from flask import Flask
from flask import jsonify
from flask import session
from flask_classful import FlaskView, route, request

from webserver.representations import output_json

from threading import Thread

from config.permanent_data import getPermanentData
from config.permanent_data import setPermanentData
from config.config import getConfig

from exceptions.invalid_api_usage import InvalidAPIUsage

from webserver.endpoints.ep_level_add import EPLevelAdd
from webserver.endpoints.ep_level_read import EPLevelRead

from webserver.endpoints.ep import EP


# -----------------------------------
#
# POST Contorl the level of the light
#
# curl  --header "Content-Type: application/json" --request POST http://localhost:5000/level/add/levelId/5/value/23.4/variance/0.0
# curl  --header "Content-Type: application/json" --request POST --data '{"levelId": "5", "value":23.4,"variance":0.0}' http://localhost:5000/level/add
#
# -----------------------------------
#
# POST http://localhost:5000/level
class LevelView(FlaskView):
    representations = {'application/json': output_json}
    inspect_args = False

    def __init__(self, web_gadget):

        self.web_gadget = web_gadget

        self.epLevelAdd = EPLevelAdd(web_gadget)
        self.epLevelRead = EPLevelRead(web_gadget)

    #
    # GET http://localhost:5000/level/
    #
    def index(self):
        return {}

# ===

    #
    # Set the level with payload
    #
    # curl  --header "Content-Type: application/json" --request POST --data '{"levelId": 5, "value":23.4,"variance":0.0}' http://localhost:5000/level/add
    #
    # POST http://localhost:5000/level/add
    #      body: {
    #            "levelId": "5",
    #            "value":23.4,
    #            "variance":0.0
    #           }
    #
    #@route('/add', methods=['POST'])
    @route(EPLevelAdd.PATH_PAR_PAYLOAD, methods=[EPLevelAdd.METHOD])
    def setWithPayload(self):

        # WEB
        if request.form:
            json_data = request.form

        # CURL
        elif request.json:
            json_data = request.json

        else:
            return "Not valid request", EP.CODE_BAD_REQUEST

        out = self.epLevelAdd.executeByPayload(json_data)
        return out

    #
    # Read the level - with parameters
    #
    # curl  --header "Content-Type: application/json" --request POST http://localhost:5000/level/add/levelId/5/value/23.4/variance/0.0
    #
    # POST http://localhost:5000/level/add/levelId/5/value/23.4/variance/0.0
    #
    #@route('/add/levelId/<levelId>/value/<value>/variance/<variance>', methods=['POST'])
    @route(EPLevelAdd.PATH_PAR_URL, methods=[EPLevelAdd.METHOD])
    def setWithParameter(self, levelId, value, variance):

        out = self.epLevelAdd.executeByParameters(levelId=levelId, value=value, variance=variance)
        return out

# ===

    #
    # Read the level - with payload
    #
    # curl  --header "Content-Type: application/json" --request GET --data '{"startDate":"2021.11.07T20:15:123+01:00"}' http://localhost:5000/level/read
    #
    # GET http://localhost:5000/level/read
    #      body: {
    #            "startDate":"2021.11.07T20:15:123+01:00"
    #           }
    #
    #@route('/read', methods=['GET'])
    @route(EPLevelRead.PATH_PAR_PAYLOAD, methods=[EPLevelRead.METHOD])
    def readWithPayload(self):

        # WEB
        if request.form:
            json_data = request.form

        # CURL
        elif request.json:
            json_data = request.json

        else:
            return "Not valid request", EP.CODE_BAD_REQUEST

        out = self.epLevelRead.executeByPayload(json_data)
        return out

    #
    # Read the level - with parameters
    #
    # curl  --header "Content-Type: application/json" --request GET http://localhost:5000/level/read/startDate/2021.11.07T20:15:123+01:00
    #
    # READ http://localhost:5000/level/read/startDate/2021.11.07T20:15:123+01:00
    #
    #@route('/read/startDate/<startDate>', methods=['GET'])
    @route(EPLevelRead.PATH_PAR_URL, methods=[EPLevelRead.METHOD])
    def readWithParameter(self, startDate):

        out = self.epLevelRead.executeByParameters(startDate=startDate)
        return out


# ===

