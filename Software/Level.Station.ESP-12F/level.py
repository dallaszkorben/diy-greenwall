from ultrasonic_sensor import UltrasonicSensor
from wifi_level import WifiLevel
import time
import config
import gc


gc.enable()

ip=config.getValue('webserver', 'ip')
path=config.getValue('webserver', 'path-level-report')
pinTrigger=config.getValue('level-sta', 'pin-trigger')
pinEcho=config.getValue('level-sta', 'pin-echo')
reportIntervalSec=config.getValue('level-sta', 'report-interval')

wl=WifiLevel()
wl.connectToAp()
us=UltrasonicSensor(pinTrigger, pinEcho)

gc.collect()

while True:
    dist = us.getDistanceMeanInMm()
#    print(dist)
#    dist = (123,456)

    gc.collect()

    wl.sendPost(address=ip, path=path, data='{"value",' + str(int(dist[0])) + '}')

    gc.collect()

    time.sleep(reportIntervalSec)
