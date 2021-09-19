import gc
import network
try:
    import usocket as socket
except:
    import socket

CONTENT = b"""\
HTTP/1.0 200 OK
Hello #%d from MicroPython!
"""


class WebServer:
    def __init__(self):

        gc.enable()

        self.server=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ai = socket.getaddrinfo("0.0.0.0", 80)
        print("Bind address info:", ai)
        self.addr = ai[0][-1]

    def close(self):
        #self.server.shutdown(socket.SHUT_RDWR)
        self.server.close()
        print ("closed")

    def startWeb(self):

        counter = 0

        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind(self.addr)
        self.server.listen(5)
        print("Listening, connect your browser to http://<this_host>:80/")

        while True:
            res = self.server.accept()


            gc.collect()


            client_sock = res[0]
            client_addr = res[1]

            print("Request arrived:")
            print("  Client address:", client_addr)
            print("  Client socket:", client_sock)

            req = client_sock.readline()
            print(req)
            while True:
                h = client_sock.readline()
                if h == b"" or h == b"\r\n":
                    break
                print(h)

            client_sock.send("HTTP/1.1 200 OK\n")
            client_sock.send('Content-Type: text/html\n')
            client_sock.send('Connection: close\n\n')
            client_sock.sendall(CONTENT % counter)

            client_sock.close()

            counter += 1
            print()
