import json

from flask import Flask
from flask import jsonify
from flask import session
from flask_classful import FlaskView, route, request

from wgadget.representations import output_json

from threading import Thread

from egadget.eg_light import EGLight

from exceptions.invalid_api_usage import InvalidAPIUsage

from wgadget.endpoints.ep_info_light import EPInfoLight

from wgadget.crossdomain import crossdomain

# -----------------------------------
#
# GET info
#
# curl  --header "Content-Type: application/json" --request GET http://localhost:5000/info/actuatorId/1
# -----------------------------------
#
# GET http://localhost:5000/info
class InfoView(FlaskView):
    representations = {'application/json': output_json}
    inspect_args = False

    def __init__(self, web_gadget):

        self.web_gadget = web_gadget

#        self.epInfoLight = EPInfoLight(web_gadget)

    #
    # GET http://localhost:5000/info/
    #
    def index(self):
        return {}

# ===

    #
    # Get the light level
    #
    # curl  --header "Content-Type: application/json" --request GET http://localhost:5000/info/actuatorId/1
    #
    # GET http://localhost:5000/info/actuatorId/1
    #
    #@route('/actuatorId/<actuatorId>', methods=['GET'])
    @route(EPInfoLight.URL_ROUTE_PAR_URL, methods=[EPInfoLight.METHOD])
    def getInfoLight(self, actuatorId):

        resp = self.epInfoLight.executeByParameters(actuatorId=actuatorId)
        result = json.dumps(resp) 
        return result


