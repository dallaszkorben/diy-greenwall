import json

from flask import Flask
from flask import jsonify
from flask import session
from flask_classful import FlaskView, route, request

from webserver.representations import output_json

from threading import Thread

from exceptions.invalid_api_usage import InvalidAPIUsage

from webserver.endpoints.ep_info_request import EPInfoRequest

# -----------------------------------
#
# GET info
#
# curl  --header "Content-Type: application/json" --request GET http://localhost:5000/info/request
# -----------------------------------
#
# GET http://localhost:5000/info
class InfoView(FlaskView):
    representations = {'application/json': output_json}
    inspect_args = False

    def __init__(self, web_gadget):

        self.web_gadget = web_gadget

    #
    # GET http://localhost:5000/info/
    #
    def index(self):
        return {}

    #
    # Get the info about possible requests
    #
    # curl  --header "Content-Type: application/json" --request GET http://localhost:5000/info/request
    #
    # GET http://localhost:5000/info/request
    #
    #@route('/request, methods=['GET'])
    @route(EPInfoRequest.URL_ROUTE_PAR_URL, methods=[EPInfoRequest.METHOD])
    def getInfoLight(self, actuatorId):

        resp = self.epInfoLight.executeByParameters(actuatorId=actuatorId)
        result = json.dumps(resp) 
        return result
