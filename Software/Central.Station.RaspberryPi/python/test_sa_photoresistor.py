#! /usr/bin/python3

import os
from time import sleep
from senact.sa_photoresistor import PhotoResistor
#from egadget.eg_light import EGLight

import logging
from logging.handlers import RotatingFileHandler

#test
if __name__ == "__main__":

    pr = PhotoResistor(1, 24)

    try:
        # Main loop
        while True:
            print(pr.measure())
    except KeyboardInterrupt:
        pass
    finally:
        pr.unconfigure()









