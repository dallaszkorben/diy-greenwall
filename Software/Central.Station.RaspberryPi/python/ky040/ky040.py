from __future__ import print_function
import evdev
import select
import threading


class KY040():

    def __init__(self, callbackUp, callbackDown, callbackEnter):

        self.callbackUp = callbackUp
        self.callbackDown = callbackDown
        self.callbackEnter = callbackEnter

        self.devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]
        self.devices = {dev.fd: dev for dev in self.devices}

    def start(self):

        x = threading.Thread(target=self.listenToInput)
        x.start()

    def listenToInput(self):

        while True:

            r, w, x = select.select(self.devices, [], [])

            for fd in r:
                for event in self.devices[fd].read():

                    event = evdev.util.categorize(event)
                    if isinstance(event, evdev.events.RelEvent):
                        if event.event.value == 1:
                            self.callbackUp()
                        else:
                            self.callbackDown()

                    elif isinstance(event, evdev.events.KeyEvent):
                        if event.keycode == "KEY_ENTER" and event.keystate == event.key_up:
                            self.callbackEnter()
