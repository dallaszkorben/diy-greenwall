#! /usr/bin/python3

from time import sleep
from senact.sa_ky040 import SAKy040
import logging

#test
if __name__ == "__main__":

    ID = 1

    CLOCK_PIN = 17
    DATA_PIN = 27
    SWITCH_PIN = 23

    def rotaryChange(value):
        print( "turned - ", str(value))

    def switchPressed():
        print ("button pressed")

    ky040 = SAKy040(ID, CLOCK_PIN, DATA_PIN, SWITCH_PIN)
    ky040.setRotaryCallbackMethod(rotaryChange)
    ky040.setSwitchCallbackMethod(switchPressed)
    ky040.configure()

    print(ky040.getSenactId())
    try:
        while True:
            sleep(10)
    finally:
        ky040.unconfigure()
