import RPi.GPIO as GPIO
import threading
import time

PUMP_TIME_IN_SEC = 5

class Pump:

    DIVIDER = 10.0
    INCREASER = 1 / DIVIDER


    def __init__(self, id, gpio):
        self.gpio = gpio

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(gpio, GPIO.OUT)

        self.pumpLock = threading.Lock()
        self.mustStopPumpLock = threading.Lock()

        self.pumpStopped = True

    def runThreadCounter(self, runInSec):
        with self.pumpLock:

            # start the pump
            GPIO.output(self.gpio, True)

            print("pump started" )

            with self.mustStopPumpLock:
                self.pumpStopped = False

            counter = 0
            while counter < runInSec and not self.pumpStopped:

                time.sleep(Pump.INCREASER)
                counter += Pump.INCREASER

            GPIO.output(self.gpio, False)

            with self.mustStopPumpLock:
                self.pumpStopped = True

            print("pump stopped")
            print()
            time.sleep(1)


    def triggerPump(self, lengthInSec=PUMP_TIME_IN_SEC):

        # No thread to pump
        if self.pumpStopped:

            # start the counter
            x = threading.Thread(target=self.runThreadCounter, args=(lengthInSec,))
            x.start()

        else:
            print("Not possible to pump")

    def stopPump(self):
        with self.mustStopPumpLock:
            self.pumpStopped = True


    def fillUp(self):
        """
        1. read the level of Tank
        2. read lhe level of all Stations
        3. write into file: fillUp started
        4. loop until 
                Tank has Minimum Level and
                Stations level not rising anymore
        5.        triggerPump()
        6.        wait for new reports from stations
        7. write into file: fillUp endded
        8. write warning if the Tank level is too low
        """
        pass