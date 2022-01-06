from lcddriver.lcddriver import lcd as Lcd
from ky040.ky040 import KY040
from lcdmenu.lcdmenu import LcdSubMenu, LcdSubElement, LcdRootMenu
from lcdmenu.lcdmenu import *
import time
from datetime import datetime
import threading

class Controlbox:

    def __init__(self, web_gadget):

        self.webGadget = web_gadget

        self.counterLock = threading.Lock()

#        lcd = Lcd()
#        maxLine = 2

        self.rootMenu=LcdRootMenu()

        self.dataMenu = LcdSubMenu( "Actual data" )
        subMenu2 = LcdSubMenu( "Control" )
        subMenu3 = LcdSubMenu( "Alerts" )
        self.rootMenu.addLcdMenu(self.dataMenu)
        self.rootMenu.addLcdMenu(subMenu2)
        self.rootMenu.addLcdMenu(subMenu3)

# ------ Show actual data -------

#        subMenu11 = LcdSubMenu( "Station 10" )
#        subMenu12 = LcdSubMenu( "Station 11" )
#        subMenu13 = LcdSubMenu( "Station 12" )
#        self.subMenu1.addLcdMenu(subMenu11)
#        self.subMenu1.addLcdMenu(subMenu12)
#        self.subMenu1.addLcdMenu(subMenu13)

#        

#        subMenu111 = LcdSubElement("  h:  35mm")
#        subMenu112 = LcdSubElement("  t:  23" + chr(223) + "C")
#        subMenu113 = LcdSubElement("  rh: 30%")
#        subMenu11.addLcdMenu(subMenu111)
#        subMenu11.addLcdMenu(subMenu112)
#        subMenu11.addLcdMenu(subMenu113)

# ------ Control actuators -------

        subMenu21 = LcdSubElement( " Pump On", self.turnPumpOn )
        subMenu22 = LcdSubElement( " Pump Off", self.turnPumpOff )
        subMenu23 = LcdSubElement( " Light On", self.turnLampOn )
        subMenu24 = LcdSubElement( " Light Off", self.turnLampOff )
        subMenu2.addLcdMenu(subMenu21)
        subMenu2.addLcdMenu(subMenu22)
        subMenu2.addLcdMenu(subMenu23)
        subMenu2.addLcdMenu(subMenu24)

        self.rootMenu.initialize()

#        self.rootMenu.showMenu()
        showMenu(self.rootMenu)

        ky040 = KY040(self.functionUp, self.functionDown, self.functionEnter)
        ky040.start()

        self.resetCounter()

        x = threading.Thread(target=self.watchdog, args=(3,))
        x.start()

#        x = threading.Thread(target=self.refreshAllData)
#        x.start()

    def resetCounter(self):
        with self.counterLock:
            self.counter = 0

    def incrementCounter(self, sleepValue):
        with self.counterLock:
            self.counter += sleepValue

    def functionUp(self):
        self.resetCounter()
        self.rootMenu.up()
#        self.rootMenu.showMenu()

    def functionDown(self):
        self.resetCounter()
        self.rootMenu.down()
#        self.rootMenu.showMenu()

    def functionEnter(self):
        self.resetCounter()
        self.rootMenu.enter()
#        self.rootMenu.showMenu()

    def turnPumpOn(self):
        print("pump ON")

    def turnPumpOff(self):
        print("pump OFF")

    def turnLampOn(self):
        print("lamp ON")

    def turnLampOff(self):
        print("lamp OFF")

    def getStationMenu(self, stationId):
        stationMenu = None
        START = 1
        for index, subMenu in enumerate(self.dataMenu.menuList[START:], START):

            # the stationId exists
            if subMenu.text == "Station " + stationId:
                stationMenu = subMenu
                break

        # the stationMenu does not exist
        if not stationMenu:

            # have to create the menu
            stationMenu = LcdSubMenu( "Station " + stationId )

            levelMenu =       LcdSubElement("levl: ")
            temperatureMenu = LcdSubElement("temp: ")
            humidityMenu =    LcdSubElement("relh: ")
            dateMenu =        LcdSubElement("date: ")
            ipMenu =          LcdSubElement("ip:   ")

            stationMenu.addLcdMenu(levelMenu)
            stationMenu.addLcdMenu(temperatureMenu)
            stationMenu.addLcdMenu(humidityMenu)
            stationMenu.addLcdMenu(dateMenu)
            stationMenu.addLcdMenu(ipMenu)

            self.dataMenu.addLcdMenu(stationMenu)

            if self.dataMenu and not self.dataMenu.startRelativeWindow == None:
#                self.dataMenu.showMenu()
                showMenu(self.dataMenu)

        return stationMenu

    def refreshLatestValues(self, latestValues):

        # go through the latestValues list
        for i in latestValues:
            si = i["stationId"]
            ip = i["ip"]
            timeStamp = i['timeStamp']
            levelValue = i['levelValue']
            temperatureValue = i['temperatureValue']
            humidityValue = i['humidityValue']

            dateString = datetime.fromtimestamp(timeStamp).astimezone().isoformat()

            stationMenu = self.getStationMenu(si)

            # water level
            stationMenu.menuList[1].setText("levl: {0} mm".format(levelValue))

            # temperature
            stationMenu.menuList[2].setText("temp: {0} {1}C".format(temperatureValue, chr(223)))

            # humidity
            stationMenu.menuList[3].setText("relh: {0} %".format(humidityValue))

            # date
            stationMenu.menuList[4].setText("date: {0}".format(dateString))
            stationMenu.menuList[4].setRotateAt(6)

            # ip
            stationMenu.menuList[5].setText("ip: {0}".format(ip))
            stationMenu.menuList[5].setRotateAt(4)

            if stationMenu.activeMenu and not stationMenu.startRelativeWindow == None:
#                stationMenu.showMenu()
                showMenu(stationMenu)

    def refreshData(self, stationId):
        latestValues = self.webGadget.report.getLatestValues(stationId)
        self.refreshLatestValues(latestValues)

    def refreshAllData(self):
        latestValues = self.webGadget.report.getLatestValues()
        self.refreshLatestValues(latestValues)

    def watchdog(self, waitInSec):
        sleepValue = 0.1

        self.resetCounter()
        while True:

            while self.counter <= waitInSec:

                time.sleep(sleepValue)
                self.incrementCounter(sleepValue)

            # circulating starts
            shift = 0
            while self.counter != 0:
                shift += 1
                showMenu(self.rootMenu,shift=shift, clear=False)
                time.sleep(0.2)
#            showMenu(self.rootMenu)
