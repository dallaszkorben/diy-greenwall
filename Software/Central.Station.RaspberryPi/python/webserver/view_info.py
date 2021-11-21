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
from webserver.endpoints.ep_info_graph import EPInfoGraph
from webserver.endpoints.ep_info_timestamp import EPInfoTimeStamp

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
        self.epInfoGraph = EPInfoGraph(web_gadget)
        self.epInfoTimeStamp = EPInfoTimeStamp(web_gadget)

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
    # Get graph - with payload
    #
    # curl  --header "Content-Type: application/json" --request GET --data '{"startDate":"2021.11.07T20:15:123+01:00"}' http://localhost:5000/info/graph
    #
    # GET http://localhost:5000/info/graph
    #      body: {
    #            "startDate":"2021.11.07T20:15:123+01:00"
    #           }
    #
    #@route('/graph', methods=['GET'])
    @route(EPInfoGraph.PATH_PAR_PAYLOAD, methods=[EPInfoGraph.METHOD])
    def infoGraphWithPayload(self):

        # WEB
        if request.form:
            json_data = request.form

        # CURL
        elif request.json:
            json_data = request.json

        else:
            return "Not valid request", EP.CODE_BAD_REQUEST

        out = self.epInfoGraph.executeByPayload(json_data)
        return out

    #
    # Get graph - with parameters
    #
    # curl  --header "Content-Type: application/json" --request GET http://localhost:5000/info/graph/startDate/2021.11.07T20:15:123+01:00
    #
    # READ http://localhost:5000/info/graph/startDate/2021.11.07T20:15:123+01:00
    #
#    #@route('/graph/startDate/<startDate>/sensorId/<sensorId>', methods=['GET'])
    #@route('/graph/startDate/<startDate>', methods=['GET'])
    @route(EPInfoGraph.PATH_PAR_URL, methods=[EPInfoGraph.METHOD])
#    def infoGraphWithParameter(self, startDate, sensorId):
    def infoGraphWithParameter(self, startDate):

        out = self.epInfoGraph.executeByParameters(startDate=startDate)
#        out = self.epInfoGraph.executeByParameters(startDate=startDate, sensorId=sensorId)
        return out


# ===

    #
    # Get actual timestamp by the epoc - with payload
    #
    # curl  --header "Content-Type: application/json" --request GET --data '{"epocDate":"2000.00.00T00:00:00"}' http://localhost:5000/info/timeStamp
    #
    # GET http://localhost:5000/info/timeStamp
    #      body: {
    #            "epocDate":"2000.00.00T00:00:00"
    #           }
    #
    #@route('/timeStamp', methods=['GET'])
    @route(EPInfoTimeStamp.PATH_PAR_PAYLOAD, methods=[EPInfoTimeStamp.METHOD])
    def infoTimeStampWithPayload(self):

        # WEB
        if request.form:
            json_data = request.form

        # CURL
        elif request.json:
            json_data = request.json

        else:
            return "Not valid request", EP.CODE_BAD_REQUEST

        out = self.epInfoTimeStamp.executeByPayload(json_data)
        return out

    #
    # Get actual timestamp by the epoc - with parameters
    #
    # curl  --header "Content-Type: application/json" --request GET http://localhost:5000/info/timeStamp/epocDate/2000.00.00T00:00:00
    #
    # READ http://localhost:5000/info/timeStamp/epocDate/2000.00.00T00:00:00
    #
    #@route('/timeStamp/epocDate/<epocDate>', methods=['GET'])
    @route(EPInfoTimeStamp.PATH_PAR_URL, methods=[EPInfoTimeStamp.METHOD])
    def infoTimeStampWithParameter(self, epocDate):

        out = self.epInfoTimeStamp.executeByParameters(epocDate)
        return out

