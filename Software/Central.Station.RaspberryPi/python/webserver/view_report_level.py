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

from webserver.endpoints.ep_reportlevel_add import EPReportLevelAdd

# -----------------------------------
#
# POST Contorl the level of the light
#
# curl  --header "Content-Type: application/json" --request POST http://localhost:5000/reportlevel/add/levelId/5/value/23.4/variance/0.0
# curl  --header "Content-Type: application/json" --request POST --data '{"levelId": "5", "value":23.4,"variance":0.0}' http://localhost:5000/reportlevel/add
#
# -----------------------------------
#
# POST http://localhost:5000/reportlevel
class ReportlevelView(FlaskView):
    representations = {'application/json': output_json}
    inspect_args = False

    def __init__(self, web_gadget):

        self.web_gadget = web_gadget

        self.epLevelAdd = EPReportLevelAdd(web_gadget)

    #
    # GET http://localhost:5000/reportlevel/
    #
    def index(self):
        return {}

# ===

    #
    # Set the level with payload
    #
    # curl  --header "Content-Type: application/json" --request POST --data '{"levelId": 5, "value":23.4,"variance":0.0}' http://localhost:5000/reportlevel/add
    #
    # POST http://localhost:5000/reportlevel/add
    #      body: {
    #            "levelId": "5",
    #            "value":23.4,
    #            "variance":0.0
    #           }
    #
    #@route('/add', methods=['POST'])
    @route(EPReportLevelAdd.PATH_PAR_PAYLOAD, methods=[EPReportLevelAdd.METHOD])
    def setWithPayload(self):

        # WEB
        if request.form:
            json_data = request.form

        # CURL
        elif request.json:
            json_data = request.json

        else:
            return "Not valid request", 400

        resp = self.epLevelAdd.executeByPayload(json_data)
#        result = json.dumps(resp) 
        return resp

    #
    # Set the level
    #
    # curl  --header "Content-Type: application/json" --request POST http://localhost:5000/reportlevel/add/levelId/5/value/23.4/variance/0.0
    #
    # POST http://localhost:5000/reportlevel/add/levelId/5/value/23.4/variance/0.0
    #
    #@route('/add/levelId/<levelId>/value/<value>/variance/<variance>', methods=['POST'])
    @route(EPReportLevelAdd.PATH_PAR_URL, methods=[EPReportLevelAdd.METHOD])
    def set(self, levelId, value, variance):

        resp = self.epLevelAdd.executeByParameters(levelId=levelId, value=value, variance=variance)
#        result = json.dumps(resp) 
        return resp

