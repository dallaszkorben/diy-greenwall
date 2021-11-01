#! /usr/bin/python3

import RPi.GPIO as GPIO
from time import sleep
from time import time
from threading import Thread
from threading import Lock
from senact.senact import SenAct

import logging

#if __name__ == "__main__":
#from sa import SA
#else:
from senact.sa import SA

class SAKy040(SA):

    INCREASE_SLOW = 1
    INCREASE_FAST = 10

    DECREASE_SLOW = -1
    DECREASE_FAST = -10
    STANDBY = 0

    MIN_DIFF_TIME = 0.1

    SENACT_TYPE = SenAct.SENSOR

    def __init__(self, id, clockPin, dataPin, switchPin, rotaryCallbackMethod=None, switchCallbackMethod=None):

        self.lock = Lock()

        GPIO.setmode(GPIO.BCM)

        self.id = id
        self.clockPin = clockPin
        self.dataPin = dataPin
        self.switchPin = switchPin
        self.rotaryCallbackMethod = rotaryCallbackMethod
        self.switchCallbackMethod = switchCallbackMethod

        #setup pins
        GPIO.setup(self.clockPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.dataPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.switchPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        self.last_change = 0
        self.last_change_time = time()

    def getSenactType(self):
        return self.__class__.SENACT_TYPE

    def getSenactId(self):
        return self.id

    def setRotaryCallbackMethod(self, rotaryCallbackMethod):
        self.rotaryCallbackMethod = rotaryCallbackMethod

    def setSwitchCallbackMethod(self, switchCallbackMethod):
        self.switchCallbackMethod = switchCallbackMethod

    def configure(self):

        GPIO.add_event_detect(self.clockPin,
                              GPIO.FALLING,
                              callback=self._clockFallingCallback,
                              bouncetime=50)

        GPIO.add_event_detect(self.dataPin,
                              GPIO.FALLING,
                              callback=self._dataFallingCallback,
                              bouncetime=50)

        GPIO.add_event_detect(self.switchPin,
                              GPIO.FALLING,
                              callback=self._switchCallback,
                              bouncetime=350)

    def unconfigure(self):

        logging.error("unconfigure ky040")

        GPIO.remove_event_detect(self.clockPin)
        GPIO.remove_event_detect(self.dataPin)
        GPIO.remove_event_detect(self.switchPin)
        GPIO.cleanup()


    # control clockwise turn
    def _clockFallingCallback(self, pin):


        if GPIO.input(self.dataPin) == 1:

            with self.lock:

                current_time = time()
                diff = current_time - self.last_change_time

                change = self.STANDBY

                # if more than 1 sec elapsed since the last change
                if(diff >= self.__class__.MIN_DIFF_TIME):

                    # then anything this operation is allowed with normal speed
                    change = self.__class__.INCREASE_SLOW

                # if less than 1 sec elapsed since the last change 
                # and the previous direction was clockwise
                elif self.last_change > 0 :

                    # then only 
                    change = self.__class__.INCREASE_FAST

                if self.rotaryCallbackMethod and not change == self.STANDBY:

                    logging.debug( "Received 1->0 on KY040 'CLOCK' PIN #{0} while 1 on 'DATA' PIN #{1} (clockwise turn) Change: {3} --- FILE: {2}".format(
                        self.clockPin,
                        self.dataPin,
                        __file__,
                        change)
                    )

                    self.last_change = change
                    self.last_change_time = time()
                    self.rotaryCallbackMethod(change)

        else:
            pass

    # counter clockwise turn
    def _dataFallingCallback(self, pin):


        if GPIO.input(self.clockPin) == 1:

            with self.lock:


                current_time = time()
                diff = current_time - self.last_change_time

                change = self.STANDBY

                # if more than 1 sec elapsed since the last change
                if(diff >= self.__class__.MIN_DIFF_TIME):

                    # then anything this operation is allowed with normal speed
                    change = self.__class__.DECREASE_SLOW

                # if less than 1 sec elapsed since the last change 
                # and the previous direction was counter clockwise
                elif self.last_change < 0 :

                    # then only 
                    change = self.__class__.DECREASE_FAST

                if self.rotaryCallbackMethod and not change == self.STANDBY:

                    logging.debug( "Received 1->0 on KY040 'DATA' PIN #{0} while 1 on 'CLOCK' PIN #{1} (counter clockwise turn) Change: {3} --- FILE: {2}".format(
                        self.dataPin,
                        self.clockPin,
                        __file__,
                        change)
                    )

                    self.last_change = change
                    self.last_change_time = time()
                    self.rotaryCallbackMethod(change)

        else:
            pass

    def _switchCallback(self, pin):

        if GPIO.input(self.switchPin) == 0:

            with self.lock:

                logging.debug( "Received 0 on KY040 switch PIN #{0} --- FILE: {1}".format(
                    self.switchPin,
                    __file__)
                )

                if self.switchCallbackMethod:

                    self.switchCallbackMethod()
