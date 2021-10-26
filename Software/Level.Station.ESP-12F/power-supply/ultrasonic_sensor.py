import machine, time
from machine import Pin
import math
class UltrasonicSensor():

    MAX_DISTANCE_IN_M = 1.0		# 1 m max distance

    def __init__(self, triggerGpio, echoGpio, zeroLevel, m, b, sampleNumber):

        self.trigger = Pin(triggerGpio, mode=Pin.OUT, pull=None)
        self.echo = Pin(echoGpio, mode=Pin.IN, pull=None)
        self.echo_timeout_us=int(1000000*UltrasonicSensor.MAX_DISTANCE_IN_M/347.125) # calculate time for 1m max distance
        self.zeroLevel = zeroLevel
        self.sampleNumber = sampleNumber

        self.m = m
        self.b = b

    def getPulse(self):
       self.trigger.value(0) 
       time.sleep_us(5)
       self.trigger.value(1)
       time.sleep_us(20)
       self.trigger.value(0)

       try:
          pulse_time = machine.time_pulse_us(self.echo, 1, self.echo_timeout_us)
          return pulse_time
       except OSError as ex:
          print("exception: ", ex)
          if ex.args[0] == 110: 
             raise OSError('Out of range')
             raise ex

    def getDistanceInMm(self):
        time.sleep_us(2000)
        pulse = self.getPulse()
        return (int(self.m * pulse + self.b), pulse)

    def getDistanceMeanInMm(self):

        distanceList = [self.getDistanceInMm()[0] for x in range(self.sampleNumber)]

        # Number of observations
        n = len(distanceList)

        # Mean of the data
        mean = sum(distanceList) / n

        # Square deviations
        deviations = [(x - mean) ** 2 for x in distanceList]

        # Variance
        variance = math.sqrt( sum(deviations) / n )

        return (mean, variance)

    def getLevelMeanInMm(self):
        dist = self.getDistanceMeanInMm()
        return (self.zeroLevel - dist[0], dist[1])