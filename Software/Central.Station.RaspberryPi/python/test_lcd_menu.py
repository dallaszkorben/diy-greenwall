from lcddriver.lcddriver import lcd as Lcd
from ky040.ky040 import KY040
from lcdmenu.lcdmenu import LcdSubMenu, LcdSubElement, LcdRootMenu
from lcdmenu.lcdmenu import *
import time
from datetime import datetime
import threading

class Controlbox:

    def __init__(self):

        self.counterLock = threading.Lock()

        self.rootMenu=LcdRootMenu()

        self.dataMenu = LcdSubMenu( "1: Ez egy nagyon hosszu menu", rotateAt=3 )
        subMenu2 = LcdSubElement( "2: Ez pedig egy hosszu elem/adat", rotateAt=3 )
        subMenu3 = LcdSubMenu( "Alerts" )
        self.rootMenu.addLcdMenu(self.dataMenu)
        self.rootMenu.addLcdMenu(subMenu2)
        self.rootMenu.addLcdMenu(subMenu3)

        self.rootMenu.initialize()

#        self.rootMenu.showMenu()
        showMenu(self.rootMenu)

        ky040 = KY040(self.functionUp, self.functionDown, self.functionEnter)
        ky040.start()

        self.resetCounter()

        x = threading.Thread(target=self.watchdog, args=(3,))
        x.start()

    def resetCounter(self):
        with self.counterLock:
            self.counter = 0

    def incrementCounter(self, sleepValue):
        with self.counterLock:
            self.counter += sleepValue

    def functionUp(self):
        self.resetCounter()
        self.rootMenu.up()

    def functionDown(self):
        self.resetCounter()
        self.rootMenu.down()

    def functionEnter(self):
        self.resetCounter()
        self.rootMenu.enter()

    def watchdog(self, waitInSec):
        sleepValue = 0.1

        self.resetCounter()
        while True:

            while self.counter <= waitInSec:

                time.sleep(sleepValue)
                self.incrementCounter(sleepValue)

            shift = 0
            while self.counter != 0:
                shift += 1
                showMenu(self.rootMenu,shift=shift, clear=False)
                time.sleep(0.2)
#            showMenu(self.rootMenu)


cb = Controlbox()
while True:
    time.sleep(0.2)