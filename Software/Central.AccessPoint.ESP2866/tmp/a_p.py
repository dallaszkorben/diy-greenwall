#################################
#
# Access Point
#
#################################

import network

HIDDEN=False

ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid='Central-Station-006', password="viragfal", hidden=HIDDEN)
#ap.config(essid='Central-Station-001', authmode=0, hidden=HIDDEN)

while ap.active() == False:
  pass

print('Connection successful')
print(ap.config("essid"))
print(ap.ifconfig())


