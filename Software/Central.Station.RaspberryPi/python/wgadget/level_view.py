import json

#from flask_api import status

from flask import Flask
from flask import jsonify
from flask import session
from flask_classful import FlaskView, route, request

from wgadget.representations import output_json

from threading import Thread

from egadget.eg_light import EGLight

from config.config_exchange import getConfigExchange
from config.config_exchange import setConfigExchange
from config.config_egadget import getConfigEGadget

from exceptions.invalid_api_usage import InvalidAPIUsage

from wgadget.endpoints.ep_level_set import EPLevelSet

#from wgadget.crossdomain import crossdomain

# -----------------------------------
#
# POST Contorl the level of the light
#
# curl  --header "Content-Type: application/json" --request POST http://localhost:5000/level/set/levelId/5/value/23.4/variance/0.0
# curl  --header "Content-Type: application/json" --request POST --data '{"levelId": 5, "value":23.4,"variance":0.0}' http://localhost:5000/level/set
#
# -----------------------------------
#
# GET http://localhost:5000/level
class LevelView(FlaskView):
    representations = {'application/json': output_json}
    inspect_args = False

    def __init__(self, web_gadget):

        self.web_gadget = web_gadget

        self.epLevelSet = EPLevelSet(web_gadget)


    #
    # GET http://localhost:5000/level/
    #
    def index(self):
        return {}

# ===

    #
    # Set the light value immediately with payload
    #
    # curl  --header "Content-Type: application/json" --request POST --data '{"levelId": 5, "value":23.4,"variance":0.0}' http://localhost:5000/level/set
    #
    # POST http://localhost:5000/level/set
    #      body: {
    #            "levelId": 5,
    #            "value":23.4,
    #            "variance":0.0
    #           }
    #
    #@route('/set', methods=['POST'])
    @route(EPLevelSet.URL_ROUTE_PAR_PAYLOAD, methods=[EPLevelSet.METHOD])
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
    # Set the light value immediately
    #
    # curl  --header "Content-Type: application/json" --request POST http://localhost:5000/level/set/levelId/5/value/23.4/variance/0.0
    #
    # POST http://localhost:5000/level/set/levelId/5/value/23.4/variance/0.0
    #
    #@route('/set/levelId/<levelId>/value/<value>/variance/<variance>', methods=['POST'])
    @route(EPLevelSet.URL_ROUTE_PAR_URL, methods=[EPLevelSet.METHOD])
    def set(self, levelId, value, variance):

        resp = self.epLevelSet.executeByParameters(levelId=levelId, value=value, variance=variance)
        result = json.dumps(resp) 
        return result

