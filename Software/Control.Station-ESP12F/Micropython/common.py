import config
from machine import Pin, PWM

def getOffsetDateString(date):
    return "{0:04d}-{1:02d}-{2:02d}T{3:02d}:{4:02d}:{5:02d}".format(date[0], date[1], date[2], date[3], date[4], date[5] )

class LedControl():

    MAX_DUTY = 1023

    INVERSE = config.getValue('control-sta', 'led-status-inverse')

    # off
    STATUS_INIT = {
        "freq": 100,
        "duty": (MAX_DUTY-0) if INVERSE else 0
    }

    # Blinking fast (short)
    STATUS_BEFORE_CONNECTION = {
        "freq": 5,
        "duty": (MAX_DUTY-20) if INVERSE else 20
    }

    STATUS_PASSED_CONNECTION = {
        "freq": 1,
        "duty": (MAX_DUTY-100) if INVERSE else 100
    }

    # Blinking 50% - 50%
    STATUS_FAILED_CONNECTION = {
        "freq": 1,
        "duty": (MAX_DUTY-500) if INVERSE else 800
    }

    # Blinking very faster (short)
    STATUS_BEFORE_SEND_REST = {
        "freq": 15,
        "duty": (MAX_DUTY-20) if INVERSE else 20
    }

    # Continous pale
    STATUS_PASSED_SEND_REST = {
        "freq": 5000,
        "duty": (MAX_DUTY-2) if INVERSE else 2
    }

    # Blinking 50% - 50%
    STATUS_FAILED_SEND_REST = {
        "freq": 1,
        "duty": (MAX_DUTY-500) if INVERSE else 500
    }

    def __init__(self):
        pinLedStatus=config.getValue('control-sta', 'led-status-gpio')
        self.led = PWM(Pin(pinLedStatus), freq=LedControl.STATUS_INIT['freq'], duty=LedControl.STATUS_INIT['duty'])

    def setBeforeConnection(self):
        self.led.freq(LedControl.STATUS_BEFORE_CONNECTION['freq'])
        self.led.duty(LedControl.STATUS_BEFORE_CONNECTION['duty'])

    def setPassedConnection(self):
        self.led.freq(LedControl.STATUS_PASSED_CONNECTION['freq'])
        self.led.duty(LedControl.STATUS_PASSED_CONNECTION['duty'])

    def setFailedConnection(self):
        self.led.freq(LedControl.STATUS_FAILED_CONNECTION['freq'])
        self.led.duty(LedControl.STATUS_FAILED_CONNECTION['duty'])

    def setBeforeSendRest(self):
        self.led.freq(LedControl.STATUS_BEFORE_SEND_REST['freq'])
        self.led.duty(LedControl.STATUS_BEFORE_SEND_REST['duty'])

    def setPassedSendRest(self):
        self.led.freq(LedControl.STATUS_PASSED_SEND_REST['freq'])
        self.led.duty(LedControl.STATUS_PASSED_SEND_REST['duty'])

    def setFailedSendRest(self):
        self.led.freq(LedControl.STATUS_FAILED_SEND_REST['freq'])
        self.led.duty(LedControl.STATUS_FAILED_SEND_REST['duty'])


