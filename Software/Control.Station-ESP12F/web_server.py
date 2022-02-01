from representations import *
import ujson
import re
import gc


try:
  import usocket as socket
except:
  import socket

class WebServer:

    def __init__(self, lampControl):
        gc.enable()

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind(('', 80))
        self.s.listen(5)

        self.lampControl = lampControl

        gc.collect()

        self.startServer()

    def startServer(self):

        """
        request with data
            curl  --header "Content-Type: application/json" --request POST --data '{"lengthInSec": "30"}' http://192.168.50.101/lamp/on
        response with data
            b'POST /lamp/on HTTP/1.1\r\nHost: 192.168.50.101\r\nUser-Agent: curl/7.64.0\r\nAccept: */*\r\nContent-Type: application/json\r\nContent-Length: 17\r\n\r\n{"lengthInSec": "30"}'
        ---
        request with parameter
            curl  --header "Content-Type: application/json" --request POST  http://192.168.50.101/lamp/on?lengthInSec=30
        response with parameter
            b'POST /lamp/on?lengthInSec=30 HTTP/1.1\r\nHost: 192.168.50.101\r\nUser-Agent: curl/7.64.0\r\nAccept: */*\r\nContent-Type: application/json\r\n\r\n'
        """

        print("Listening ...")

        while True:
            conn, addr = self.s.accept()

            rawRequest = conn.recv(1024)
            request = rawRequest.decode("utf-8")

#            print('Got a connection from {0}, Request: {1}'.format(str(addr), request.replace("\r\n", " ")))

            if len(request) == 0:
                conn.close()
                continue

            request_lines = request.split("\r\n")

            gc.collect()

            fromAddress = addr[0]

            req = re.match("(POST|GET) (/[A-Za-z0-9\/]+)[?]*([A-Za-z0-9&=]*)", request_lines[0])
            type = req.group(1)
            path = req.group(2)
            param_string=req.group(3)

            print('Got a connection from {0}, Request: {1} {2} {3} '.format(fromAddress, type, path, param_string), end="")

            contentLengthReg = re.search("Content-Length: (\d+)", request)
            contentLength = int(contentLengthReg.group(1) if contentLengthReg else '0')

            gc.collect()

            # if there is parameter
            if param_string:

                param_list = param_string.split("&")
                for i in param_list:
                    par_pair = i.split("=")
                    locals()[par_pair[0]] = par_pair[1]

            # if there is data
            elif contentLength > 0 and request_lines[-1]:

                param_json = ujson.loads(request_lines[-1])
                for param_key in param_json:
                    locals()[param_key] = param_json.get(param_key)

            gc.collect()

            response = ujson.dumps(output_json(success=True))
            if type == "POST" and path == "/lamp/on":

                if 'lengthInSec' in locals():
                    lengthInSec = int(locals()['lengthInSec'])
                else:
                    lengthInSec = 0

#                self.lampControl.on(lengthInSec)

            elif type == "POST" and path == "/lamp/off":

                if 'lengthInSec' in locals():
                    lengthInSec = int(locals()['lengthInSec'])
                else:
                    lengthInSec = 0

#                self.lampControl.off(lengthInSec)

            else:
                response = ujson.dumps(output_json(success=False))

            gc.collect()

            conn.send('HTTP/1.1 200 OK\n')
            conn.send('Content-Type: text/html\n')
            conn.send('Connection: close\n\n')
            conn.sendall(response)
            conn.close()

            if type == "POST" and path == "/lamp/on":

                self.lampControl.on(lengthInSec)

            elif type == "POST" and path == "/lamp/off":

                self.lampControl.off(lengthInSec)

#            print("--- {0} {1} {2}".format(type, path, lengthInSec))

        print("Finished listening ...")
        self.s.close()