from micropyserver import MicroPyServer
import json

def return_json(request):
    ''' request handler '''
    json_str = json.dumps({"param_one": 1, "param_two": 2})
    server.send("HTTP/1.0 200 OK\r\n")
    server.send("Content-Type: application/json\r\n\r\n")
    server.send(json_str)

server = MicroPyServer()

server.add_route("/", return_json)


server.start()
