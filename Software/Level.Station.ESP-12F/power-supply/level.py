#from sensor_level_hcsr04 import SensorLevel
#from water_level_sensor import WaterLevelSensor
from wifi_level import WifiLevel
import time
import config
import gc
import machine
from machine import Timer
import utime

import ujson

def setTime():

    result = {'success': False}

    while not result['success']:
        #timeutime.localtime(0)
        epocDate = "2000.01.01"
        #data = ujson.dumps({'epocDate': epocDate})
        result = wl.sendRest(type="GET", address=ip, path=path_info_timestamp + "/epocDate/" + epocDate) #, data=data)
        time.sleep(1)

#    print(result)

    timeStamp = result['data']['timeStamp']
    date = utime.localtime(timeStamp)
    correctedDate = (date[0], date[1], date[2], 0, date[3], date[4], date[5], 0)
    machine.RTC().datetime(correctedDate)

#    timeStamp = result['timeStamp']
#    print(timeStamp)
#    print()
#    print(result['data'])
#    print()

def getStringDate(date):
    return "{0:04d}-{1:02d}-{2:02d}T{3:02d}:{4:02d}:{5:02d}".format(date[0], date[1], date[2], date[3], date[4], date[5] )


gc.enable()

# ###########################################################
#
# Parameter Load
#
# ###########################################################

#
# central-ap
#
ip=config.getValue('central-ap', 'webserver-ip')
path_level_add=config.getValue('central-ap', 'webserver-path-level-add')
path_info_timestamp=config.getValue('central-ap', 'webserver-path-info-timestamp')

#
# level-sta
#
stationId=config.getValue('level-sta', 'station-id')
reportIntervalSec=config.getValue('level-sta', 'report-interval-sec')
resetHours=config.getValue('level-sta', 'reset-hours')
#pinAnalog=config.getValue('level-sta', 'analog-pin')

#
# sensor-level
#
sensorLevelPackageName=config.getValue('sensor-level', 'package-name')
pinTrigger=config.getValue('sensor-level', 'trigger-pin')
pinEcho=config.getValue('sensor-level', 'echo-pin')
zeroLevel=config.getValue('sensor-level', 'zero-level')
#m=config.getValue('level-sensor', 'linear-m')
#b=config.getValue('level-sensor', 'linear-b')
a=config.getValue('sensor-level', 'quadratic-a')
b=config.getValue('sensor-level', 'quadratic-b')
c=config.getValue('sensor-level', 'quadratic-c')
sampleNumber=config.getValue('sensor-level', 'sample-number')
maximumVariance=config.getValue('sensor-level', 'maximum-variance')

#
# sensor-temperature-humidity
#
sensorTempHumPackageName=config.getValue('sensor-temp-hum', 'package-name')
dataGpio=config.getValue('sensor-temp-hum', 'data-gpio')

# ###########################################################

SensorLevel=__import__(sensorLevelPackageName).SensorLevel
SensorTempHum=__import__(sensorTempHumPackageName).SensorTempHum

print()

wl=WifiLevel()
wl.connectToAp()
setTime()

#
# Depending on what kind of sensor is used
#
wls=SensorLevel(pinTrigger, pinEcho, sampleNumber, a=a, b=b, c=c, zeroLevel=zeroLevel)
#wls=WaterLevelSensor(pinAnalog, sampleNumber, m, b)

ths=SensorTempHum(dataGpio)

gc.collect()

# Have to reset the chip, because for some reson, the pythin got frozen after some hours
resetMiliseconds = resetHours * 60 * 60 * 1000 # [ms]
timer=Timer(-1)
timer.init(period=resetMiliseconds, mode=Timer.ONE_SHOT, callback=lambda t:machine.reset())

while True:

    minLevel=(None, None)
    counter = 0

    # Reading water level
    while True:

        level = wls.getLevelMeanInMm()

        phase = counter % 4
        print("-\r" if phase == 0 else "\\\r" if phase == 1 else "|\r" if phase == 2 else "/\r", end="")

        # save if it is lower than
        if minLevel[1] == None or minLevel[1] > level[1]:
            minLevel = (level[0], level[1])

        if minLevel[1] < maximumVariance:
            break

        # for long time there was NO expectable variance
        if counter > 500:
            break

        counter = counter + 1
        time.sleep_ms(1)

    # Reading Temperature and Humidity
    temp, hum = ths.getTempHum()

    data = ujson.dumps({'stationId': stationId, 'dateString': getStringDate(utime.localtime()), 'levelValue': minLevel[0], 'levelVariance': minLevel[1], 'temperatureValue': temp, 'humidityValue': hum  })
#    data = ujson.dumps({'levelId': levelId, 'value': minLevel[0], 'variance': minLevel[1], 'dateString': getStringDate(utime.localtime())})

    result = wl.sendRest(type="POST", address=ip, path=path_level_add, data=data)
    gc.collect()

    # Unsuccessful send
    if not result['success']:
        time.sleep(1)
        continue

    time.sleep(reportIntervalSec)

