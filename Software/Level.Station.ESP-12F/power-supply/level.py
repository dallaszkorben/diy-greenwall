from ultrasonic_sensor import UltrasonicSensor
from wifi_level import WifiLevel
import time
import config
import gc


gc.enable()

# ###########################################################
#
# Parameter Load
#
# ###########################################################
ip=config.getValue('webserver', 'ip')
path=config.getValue('webserver', 'path-level-report')
pinTrigger=config.getValue('level-sta', 'trigger-pin')
pinEcho=config.getValue('level-sta', 'echo-pin')
reportIntervalSec=config.getValue('level-sta', 'report-interval-sec')
# ###########################################################

wl=WifiLevel()
wl.connectToAp()
us=UltrasonicSensor(pinTrigger, pinEcho)

gc.collect()

while True:
    dist = us.getDistanceMeanInMm()

    gc.collect()

    wl.sendPost(address=ip, path=path, data='{"value":' + str(int(dist[0])) + ', "variance": ' + '{:.3f}'.format(dist[1]) + '}')

    gc.collect()

    time.sleep(reportIntervalSec)
