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
zeroLevel=config.getValue('level-sta', 'zero-level')
m=config.getValue('level-sta', 'linear-m')
b=config.getValue('level-sta', 'linear-b')
# ###########################################################

wl=WifiLevel()
#wl.connectToAp()
us=UltrasonicSensor(pinTrigger, pinEcho, zeroLevel, m, b)
print()

gc.collect()

while True:

#    print("Waiting for the next sample, ", end="")
    counter = 0
    while True:
#    dist = us.getDistanceMeanInMm()
        level = us.getLevelMeanInMm()
        gc.collect()

        phase = counter % 4
        print("-\r" if phase == 0 else "\\\r" if phase == 1 else "|\r" if phase == 2 else "/\r", end="")
        if level[1] < 0.2:
            break
        counter = counter + 1
        time.sleep_ms(100)

    result = wl.sendPost(address=ip, path=path, data='{"value":' + str(int(level[0])) + ', "variance": ' + '{:.3f}'.format(level[1]) + '}')
    gc.collect()

    if not result:
        continue

    time.sleep(reportIntervalSec)

