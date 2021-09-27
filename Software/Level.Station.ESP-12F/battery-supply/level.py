from ultrasonic_sensor import UltrasonicSensor
from power_level_sensor import PowerLevelSensor
from wifi_level import WifiLevel
import time
import config
import gc
import machine

def deepSleep(msecs):
  #configure RTC.ALARM0 to be able to wake the device
  rtc = machine.RTC()
  rtc.irq(trigger=rtc.ALARM0, wake=machine.DEEPSLEEP)
  # set RTC.ALARM0 to fire after Xmilliseconds, waking the device
  rtc.alarm(rtc.ALARM0, msecs)
  #put the device to sleep
  machine.deepsleep()


# ###########################################################
#
# Parameter Load
#
# ###########################################################

ip=config.getValue('webserver', 'ip')
path=config.getValue('webserver', 'path-level-report')
pinTrigger=config.getValue('level-sta', 'trigger-pin')
pinEcho=config.getValue('level-sta', 'echo-pin')
pinAdc=config.getValue('level-sta', 'adc-pin')
reportIntervalMsec=config.getValue('level-sta', 'report-interval-msec')
m=config.getValue('power', 'm')
b=config.getValue('power', 'b')
# ###########################################################

gc.enable()

machine.sleep(10)
wl=WifiLevel()
gc.collect()

# ###########################################################
#
# Collect Information
#
# ###########################################################
ps = PowerLevelSensor(pinAdc, m, b)
power = ps.getPowerMeanInVolt()
gc.collect()

us=UltrasonicSensor(pinTrigger, pinEcho)
dist = us.getDistanceMeanInMm()
gc.collect()

##############################################################

wl.sendPost(address=ip, path=path, data='{"distance": {"value":' + str(int(dist[0])) + ', "variance":' + '{:.3f}'.format(dist[1]) + '},"power": {"value":' + '{:.2f}'.format(power[0]) + ', "variance":' + '{:.3f}'.format(power[1]) +'}}')

gc.collect()

deepSleep(reportIntervalMsec)
