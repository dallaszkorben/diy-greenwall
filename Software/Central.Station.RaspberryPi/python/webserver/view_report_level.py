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

from webserver.endpoints.ep_reportlevel_set import EPReportLevelSet

# -----------------------------------
#
# POST Contorl the level of the light
#
# curl  --header "Content-Type: application/json" --request POST http://localhost:5000/reportlevel/set/levelId/5/value/23.4/variance/0.0
# curl  --header "Content-Type: application/json" --request POST --data '{"levelId": 5, "value":23.4,"variance":0.0}' http://localhost:5000/reportlevel/set
#
# -----------------------------------
#
# POST http://localhost:5000/reportlevel
class ReportlevelView(FlaskView):
    representations = {'application/json': output_json}
    inspect_args = False

    def __init__(self, web_gadget):

        self.web_gadget = web_gadget

        self.epLevelSet = EPReportLevelSet(web_gadget)


    #
    # GET http://localhost:5000/reportlevel/
    #
    def index(self):
        return {}

# ===

    #
    # Set the level with payload
    #
    # curl  --header "Content-Type: application/json" --request POST --data '{"levelId": 5, "value":23.4,"variance":0.0}' http://localhost:5000/reportlevel/set
    #
    # POST http://localhost:5000/reportlevel/set
    #      body: {
    #            "levelId": 5,
    #            "value":23.4,
    #            "variance":0.0
    #           }
    #
    #@route('/set', methods=['POST'])
    @route(EPReportLevelSet.URL_ROUTE_PAR_PAYLOAD, methods=[EPReportLevelSet.METHOD])
    def setWithPayload(self):

        # WEB
        if request.form:
            json_data = request.form

        # CURL
        elif request.json:
            json_data = request.json

        else:
            return "Not valid request", 400

        resp = self.epLevelSet.executeByPayload(json_data)
        result = json.dumps(resp) 
        return result

    #
    # Set the level
    #
    # curl  --header "Content-Type: application/json" --request POST http://localhost:5000/reportlevel/set/levelId/5/value/23.4/variance/0.0
    #
    # POST http://localhost:5000/reportlevel/set/levelId/5/value/23.4/variance/0.0
    #
    #@route('/set/levelId/<levelId>/value/<value>/variance/<variance>', methods=['POST'])
    @route(EPReportLevelSet.URL_ROUTE_PAR_URL, methods=[EPReportLevelSet.METHOD])
    def set(self, levelId, value, variance):

        resp = self.epLevelSet.executeByParameters(levelId=levelId, value=value, variance=variance)
        result = json.dumps(resp) 
        return result

