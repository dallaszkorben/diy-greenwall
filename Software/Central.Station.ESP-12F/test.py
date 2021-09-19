import network
try:
    import usocket as socket
except:
    import socket


def connectToAP():
    wlan=network.WLAN(network.STA_IF)
    wlan.active(True)

    if not wlan.isconnected():
        print("connecting to network...")
#        wlan.ifconfig(('192.168.4.20', '255.255.255.0', '192.168.4.1', '192.168.4.1'))
        wlan.connect("Central-Station-001", "viragfal")
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




def read(address="192.168.4.2"):
    s = socket.socket()

    ai = socket.getaddrinfo(address, 80)
    print("Address infos:", ai)
    addr = ai[0][-1]

    print("Connect address:", addr)
    s.connect(addr)

    s.send(b"GET / HTTP/1.0\r\n\r\n")
    print(s.recv(4096))

    s.close()