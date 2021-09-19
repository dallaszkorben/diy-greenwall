import network
try:
    import usocket as socket
except:
    import socket

CONTENT = b"""\
HTTP/1.0 200 OK
Hello #%d from MicroPython!
"""

def connectToAP():
    wlan=network.WLAN(network.STA_IF)
    wlan.active(True)

    if not wlan.isconnected():
        print("connecting to network...")
#        wlan.ifconfig(('192.168.4.20', '255.255.255.0', '192.168.4.1', '192.168.4.1'))
        wlan.connect("Central-Station-006", "viragfal")
        while not wlan.isconnected():
            pass
        print("connected")
        print("network config:", wlan.ifconfig())
    return wlan

def disconnectToAP():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    if wlan.isconnected():
        wlan.disconnect()

class WebServer:
    def __init__(self):

        disconnectToAP()
        connectToAP()

        self.server=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ai = socket.getaddrinfo("0.0.0.0", 80)
        print("Bind address info:", ai)
        self.addr = ai[0][-1]

    def close(self):
        #self.server.shutdown(socket.SHUT_RDWR)
        self.server.close()
        print ("closed")

    def startWeb(self, micropython_optimize=False):

        counter = 0

        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind(self.addr)
        self.server.listen(5)
        print("Listening, connect your browser to http://<this_host>:80/")

        while True:
            res = self.server.accept()
            client_sock = res[0]
            client_addr = res[1]
            print("Client address:", client_addr)
            print("Client socket:", client_sock)

            if not micropython_optimize:
                # To read line-oriented protocol (like HTTP) from a socket (and
                # avoid short read problem), it must be wrapped in a stream (aka
                # file-like) object. That's how you do it in CPython:
                client_stream = client_sock.makefile("rwb")
            else:
                # .. but MicroPython socket objects support stream interface
                # directly, so calling .makefile() method is not required. If
                # you develop application which will run only on MicroPython,
                # especially on a resource-constrained embedded device, you
                # may take this shortcut to save resources.
                client_stream = client_sock

            print("Request:")
            req = client_stream.readline()
            print(req)
            while True:
                h = client_stream.readline()
                if h == b"" or h == b"\r\n":
                    break
                print(h)
            client_stream.write(CONTENT % counter)

            client_stream.close()
            if not micropython_optimize:
                client_sock.close()
            counter += 1
            print()
