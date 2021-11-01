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

from wgadget.endpoints.ep_immediately_set_light import EPImmediatelySetLight
from wgadget.endpoints.ep_immediately_increase_light import EPImmediatelyIncreaseLight
from wgadget.endpoints.ep_immediately_reverse_light import EPImmediatelyReverseLight

#from wgadget.crossdomain import crossdomain

# -----------------------------------
#
# POST Contorl the level of the light
#
# curl  --header "Content-Type: application/json" --request POST http://localhost:5000/immediately/set/actuatorId/1/value/10
# curl  --header "Content-Type: application/json" --request POST --data '{"actuatorId":1,"value":10}' http://localhost:5000/immediately/set
#
# curl  --header "Content-Type: application/json" --request POST http://localhost:5000/immediately/increase/actuatorId/1/stepvalue/-10
# curl  --header "Content-Type: application/json" --request POST --data '{"actuatorId":1,"stepValue":-10}' http://localhost:5000/immediately/increase
# -----------------------------------
#
# GET http://localhost:5000/immediately
class ImmediatelyView(FlaskView):
    representations = {'application/json': output_json}
    inspect_args = False

    def __init__(self, web_gadget):

        self.web_gadget = web_gadget

        self.epImmediatelySetLight = EPImmediatelySetLight(web_gadget)
        self.epImmediatelyIncreaseLight = EPImmediatelyIncreaseLight(web_gadget)
        self.epImmediatelyReverseLight = EPImmediatelyReverseLight(web_gadget)

    #
    # GET http://localhost:5000/immediately/
    #
    def index(self):
        return {}

# ===

    #
    # Set the light value immediately with payload
    #
    # curl  --header "Content-Type: application/json" --request POST --data '{"actuatorId":1,"value":10}' http://localhost:5000/imediately/set
    #
    # POST http://localhost:5000/imediately/set
    #      body: {
    #                'actuatorId': 1,
    #                'value: 10
    #           }
    #
    #@route('/set', methods=['POST'])
    @route(EPImmediatelySetLight.URL_ROUTE_PAR_PAYLOAD, methods=[EPImmediatelySetLight.METHOD])
    def setWithPayload(self):

        # WEB
        if request.form:
            json_data = request.form

        # CURL
        elif request.json:
            json_data = request.json

        else:
            return "Not valid request", 400

        resp = self.epImmediatelySetLight.executeByPayload(json_data)
        result = json.dumps(resp) 
        return result

    #
    # Set the light value immediately
    #
    # curl  --header "Content-Type: application/json" --request POST http://localhost:5000/immediately/set/actuatorId/1/value/10
    #
    # POST http://localhost:5000/immediately/set/actuatorId/1/value/10
    #
    #@route('/set/actuatorId/<actuatorId>/value/<value>', methods=['POST'])
    @route(EPImmediatelySetLight.URL_ROUTE_PAR_URL, methods=[EPImmediatelySetLight.METHOD])
    def set(self, actuatorId, value):

        resp = self.epImmediatelySetLight.executeByParameters(actuatorId=actuatorId, value=value)
        result = json.dumps(resp) 
        return result

# ===

    #
    # Increase the light value immediately with payload
    #
    # curl  --header "Content-Type: application/json" --request POST --data '{"actuatorId":1,"stepValue":-10}' http://localhost:5000/immediately/increase
    #
    # POST http://localhost:5000/imediately/increase
    #      body: {
    #                'actuatorId': 1,
    #                'stepValue: -10
    #           }
    #
    #@route('/increase', methods=['POST'])
    @route(EPImmediatelyIncreaseLight.URL_ROUTE_PAR_PAYLOAD, methods=[EPImmediatelyIncreaseLight.METHOD])
    def increaseWithPayload(self):

        # WEB
        if request.form:
            json_data = request.form

        # CURL
        elif request.json:
            json_data = request.json

        else:
            return "Not valid request", 400

        resp = self.epImmediatelyIncreaseLight.executeByPayload(json_data)
        result = json.dumps(resp) 
        return result

    #
    # Increase the light value immediately
    #
    # curl  --header "Content-Type: application/json" --request POST http://localhost:5000/immediately/increase/actuatorId/1/stepValue/10
    #
    # POST http://localhost:5000/imediately/increase/actuatorId/1/stepValue/-10
    #
    #@route('/increase/actuatorId/<actuatorId>/stepValue/<stepValue>', methods=['POST'])
    @route(EPImmediatelyIncreaseLight.URL_ROUTE_PAR_URL, methods=[EPImmediatelyIncreaseLight.METHOD])
    def increase(self, actuatorId, stepValue):

        resp = self.epImmediatelyIncreaseLight.executeByParameters(actuatorId=actuatorId, stepValue=stepValue)
        result = json.dumps(resp) 
        return result

# ===

    #
    # Reverse the light value immediately with payload
    #
    # curl  --header "Content-Type: application/json" --request POST --data '{"actuatorId":"1"}' http://localhost:5000/immediately/reverse
    #
    # POST http://localhost:5000/immediately/reverse
    #      body: {
    #                'actuatorId': 1
    #           }
    #
    #@route('/reverse', methods=['POST'])
    @route(EPImmediatelyReverseLight.URL_ROUTE_PAR_PAYLOAD,  methods=[EPImmediatelyReverseLight.METHOD] )
    def reverseWithPayload(self):

        # WEB
        if request.form:
            json_data = request.form

        # CURL
        elif request.json:
            json_data = request.json

        else:
            return "Not valid request", 400

        resp = self.epImmediatelyReverseLight.executeByPayload(json_data)
        result = json.dumps(resp) 
        return result


    #
    # Reverse the light value immediately
    #
    # curl  --header "Content-Type: application/json" --request POST http://localhost:5000/immediately/reverse/actuatorId/1
    #
    # POST http://localhost:5000/immediately/reverse/actuatorId/1/
    #
    #@route('/reverse/actuatorId/<actuatorId>', methods=['POST'])
    @route(EPImmediatelyReverseLight.URL_ROUTE_PAR_URL, methods=[EPImmediatelySetLight.METHOD])
    def reverse(self, actuatorId):

        resp = self.epImmediatelyReverseLight.executeByParameters(actuatorId=actuatorId)
        result = json.dumps(resp) 
        return result
