#################################
#
# Access Point
#
#################################

import network
import gc

HIDDEN=False

gc.collect()

def createAp():
    print()
    print("***************************")
    print("Configuring Access Point...")
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    ap.config(essid='Central-Station-006', password="viragfal", hidden=HIDDEN)
    #ap.config(essid='Central-Station-001', authmode=0, hidden=HIDDEN)

    while ap.active() == False:
      pass

    print('Access Point is done')
    print("essid: ", ap.config("essid"))
    print("ifconfig: ", ap.ifconfig())
    print("***************************")

