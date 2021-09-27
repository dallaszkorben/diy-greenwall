import machine, time
from machine import ADC
import math
from conversion import getMeanAndVariance

class PowerLevelSensor():

    SAMPLE_NUMBER = 50			#Number of samples for mean value

    def __init__(self, adcGpio, m, b):

        self.adc = ADC(adcGpio)
        self.m = m
        self.b = b

    def getDigitalValue(self):
        digital_value = self.adc.read()
        return digital_value

    def getPowerInVolt(self):
        digital_value = self.getDigitalValue()
        return (digital_value * self.m + self.b, digital_value)

    def getPowerMeanInVolt(self):

        powerList = [self.getPowerInVolt()[0] for x in range(PowerLevelSensor.SAMPLE_NUMBER)]

        return getMeanAndVariance(powerList)