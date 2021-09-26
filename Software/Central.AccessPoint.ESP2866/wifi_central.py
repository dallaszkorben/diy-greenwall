from micropyserver import MicroPyServer
import json
import network
import gc

class WifiCentral():

    HIDDEN=False

    def __init__(self):
        self.server = None

        gc.collect()


        print()
        print("***************************")
        print("Configuring Access Point...")
        self.ap = network.WLAN(network.AP_IF)
        self.ap.active(True)
        self.ap.config(essid='Central-Station-006', password="viragfal", hidden=WifiCentral.HIDDEN)

        while self.ap.active() == False:
          pass

        print('Access Point is done')
        print("essid: ", self.ap.config("essid"))
        print("ifconfig: ", self.ap.ifconfig())
        print("***************************")

    def return_json(self, request, data):
        ''' request handler '''
        request

        print(data)

        json_str = json.dumps({"received": "ok"})
        self.server.send("HTTP/1.0 200 OK\r\n")
        self.server.send("Content-Type: application/json\r\n\r\n")
        self.server.send(json_str)

    def start(self):
        self.server = MicroPyServer()

        self.server.add_route("/levelreport", self.return_json, method="POST")

        try:
            self.server.start()
        finally:
            self.server.close()