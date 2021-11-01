#! /usr/bin/python3

import RPi.GPIO as GPIO
from time import sleep
from time import time
from threading import Thread
from threading import Lock
from senact.senact import SenAct

import time
import logging

from senact.sa import SA

class PhotoResistor(SA):

    SENACT_TYPE = SenAct.SENSOR

    def __init__(self, id, photoResistorPin, switchCallbackMethod=None):

        self.lock = Lock()

        GPIO.setmode(GPIO.BCM)

        self.id = id
        self.photoResistorPin = photoResistorPin
        self.switchCallbackMethod = switchCallbackMethod

        #setup pins
        #GPIO.setup(self.clockPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def getSenactType(self):
        return self.__class__.SENACT_TYPE

    def getSenactId(self):
        return self.id

    def configure(self):
        pass
#        GPIO.add_event_detect(self.switchPin,
#                              GPIO.FALLING,
#                              callback=self._switchCallback,
#                              bouncetime=350)

    def unconfigure(self):
#        GPIO.remove_event_detect(self.switchPin)
        GPIO.cleanup()

    def _switchCallback(self, pin):
        pass


    def measure(self):

        with self.lock:

            #
            # discharges the circuit
            #

            #Change the pin back to output
            GPIO.setup(self.photoResistorPin, GPIO.OUT)
            GPIO.output(self.photoResistorPin, GPIO.LOW)
            time.sleep(1) #5 tau to discarge it fully

            #
            # charge the circuit
            #

            #Change the pin back to input
            GPIO.setup(self.photoResistorPin, GPIO.IN)
            count = 0

            #Count until the pin goes high
            while (GPIO.input(self.photoResistorPin) == GPIO.LOW):
                time.sleep(0.001)
                count += 1

            return count

