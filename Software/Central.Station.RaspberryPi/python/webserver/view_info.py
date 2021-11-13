import json

from flask import Flask
from flask import jsonify
from flask import session
from flask_classful import FlaskView, route, request

from webserver.representations import output_json

#from threading import Thread

from exceptions.invalid_api_usage import InvalidAPIUsage

from webserver.endpoints.ep_info_functions import EPInfoFunctions
from webserver.endpoints.ep_info_level import EPInfoLevel
from webserver.endpoints.ep_info_trend import EPInfoTrend

# -----------------------------------
#
# GET info
#
# curl  --header "Content-Type: application/json" --request GET http://localhost:5000/info/request
# -----------------------------------
#
# GET http://localhost:5000/info
class InfoView(FlaskView):
    inspect_args = False

    def __init__(self, web_gadget):

        self.web_gadget = web_gadget

        self.epInfoFunctions = EPInfoFunctions(web_gadget)
        self.epInfoLevel = EPInfoLevel(web_gadget)
        self.epInfoTrend = EPInfoTrend(web_gadget)

    #
    # GET http://localhost:5000/info/
    #
    def index(self):
        return {}

    #
    # Get the info about possible requests
    #
    # curl  --header "Content-Type: application/json" --request GET http://localhost:5000/info/functions
    #
    # GET http://localhost:5000/info/functions
    #
    #@route('/functions, methods=['GET'])
    @route(EPInfoFunctions.PATH_PAR_URL, methods=[EPInfoFunctions.METHOD])
    def getInfoFunctions(self):

        out = self.epInfoFunctions.executeByParameters()
        return out

# ===

    #
    # Read the level - with payload
    #
    # curl  --header "Content-Type: application/json" --request GET --data '{"startDate":"2021.11.07T20:15:123+01:00"}' http://localhost:5000/info/level
    #
    # GET http://localhost:5000/info/level
    #      body: {
    #            "startDate":"2021.11.07T20:15:123+01:00"
    #           }
    #
    #@route('/level', methods=['GET'])
    @route(EPInfoLevel.PATH_PAR_PAYLOAD, methods=[EPInfoLevel.METHOD])
    def infoLevelWithPayload(self):

        # WEB
        if request.form:
            json_data = request.form

        # CURL
        elif request.json:
            json_data = request.json

        else:
            return "Not valid request", EP.CODE_BAD_REQUEST

        out = self.epInfoLevel.executeByPayload(json_data)
        return out

    #
    # Read the level - with parameters
    #
    # curl  --header "Content-Type: application/json" --request GET http://localhost:5000/level/read/startDate/2021.11.07T20:15:123+01:00
    #
    # READ http://localhost:5000/level/read/startDate/2021.11.07T20:15:123+01:00
    #
    #@route('/read/startDate/<startDate>', methods=['GET'])
    @route(EPInfoLevel.PATH_PAR_URL, methods=[EPInfoLevel.METHOD])
    def infoLevelWithParameter(self, startDate):

        out = self.epInfoLevel.executeByParameters(startDate=startDate)
        return out


# ===

    #
    # Read the trend - with payload
    #
    # curl  --header "Content-Type: application/json" --request GET --data '{"startDate":"2021.11.07T20:15:123+01:00"}' http://localhost:5000/info/trend
    #
    # GET http://localhost:5000/info/trend
    #      body: {
    #            "startDate":"2021.11.07T20:15:123+01:00"
    #           }
    #
    #@route('/trend', methods=['GET'])
    @route(EPInfoTrend.PATH_PAR_PAYLOAD, methods=[EPInfoTrend.METHOD])
    def infoTrendWithPayload(self):

        # WEB
        if request.form:
            json_data = request.form

        # CURL
        elif request.json:
            json_data = request.json

        else:
            return "Not valid request", EP.CODE_BAD_REQUEST

        out = self.epInfoTrend.executeByPayload(json_data)
        return out

    #
    # Read the trend - with parameters
    #
    # curl  --header "Content-Type: application/json" --request GET http://localhost:5000/info/trend/startDate/2021.11.07T20:15:123+01:00
    #
    # READ http://localhost:5000/info/trend/startDate/2021.11.07T20:15:123+01:00
    #
    #@route('/trend/startDate/<startDate>', methods=['GET'])
    @route(EPInfoTrend.PATH_PAR_URL, methods=[EPInfoTrend.METHOD])
    def infoTrendWithParameter(self, startDate):

        out = self.epInfoTrend.executeByParameters(startDate=startDate)
        return out

