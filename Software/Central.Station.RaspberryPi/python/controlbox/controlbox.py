from lcddriver.lcddriver import lcd as Lcd
from ky040.ky040 import KY040
from lcdmenu.lcdmenu import LcdSubMenu, LcdSubElement, LcdRootMenu
from lcdmenu.lcdmenu import *
import time
from datetime import datetime
import threading
import psutil
import socket


class Controlbox:

    def __init__(self, web_gadget):

        self.webGadget = web_gadget

        self.counterLock = threading.Lock()

        self.rootMenu=LcdRootMenu()

        self.dataMenu = LcdSubMenu( "Actual data" )
        self.controlMenu = LcdSubMenu( "Control" )
        self.alertMenu = LcdSubMenu( "Alerts" )
        self.piMenu = LcdSubMenu( "PI" )
        self.rootMenu.addLcdMenu(self.dataMenu)
        self.rootMenu.addLcdMenu(self.controlMenu)
        self.rootMenu.addLcdMenu(self.alertMenu)
        self.rootMenu.addLcdMenu(self.piMenu)

# ------ Control actuators -------

        controlMenu_1 = LcdSubElement( " Pump On", self.turnPumpOn )
        controlMenu_2 = LcdSubElement( " Pump Off", self.turnPumpOff )
        controlMenu_3 = LcdSubElement( " Light On", self.turnLampOn )
        controlMenu_4 = LcdSubElement( " Light Off", self.turnLampOff )

        self.controlMenu.addLcdMenu(controlMenu_1)
        self.controlMenu.addLcdMenu(controlMenu_2)
        self.controlMenu.addLcdMenu(controlMenu_3)
        self.controlMenu.addLcdMenu(controlMenu_4)

# ------ PI menu -------

        interfacesMenu = LcdSubMenu( "Interfaces" )
        self.piMenu.addLcdMenu(interfacesMenu)

        hostMenu = LcdSubElement( "Host: {0}".format(socket.gethostname()), rotateAt=6 )
        self.piMenu.addLcdMenu(hostMenu)


# ------ Interfaces menu -------

        ipAddresses = self.getIpAddresses()
        for interface, data in ipAddresses.items():

            if interface == "lo":
                continue

            ifMenu = LcdSubMenu(interface)
            interfacesMenu.addLcdMenu(ifMenu)

            macMenu = LcdSubElement( "mac: {0}".format(data["mac"]), rotateAt=5 )
            ifMenu.addLcdMenu(macMenu)

            ipMenu = LcdSubElement( "ip: {0}".format(data["ip"]), rotateAt=4 )
            ifMenu.addLcdMenu(ipMenu)

        self.rootMenu.initialize()

        showMenu(self.rootMenu)

        ky040 = KY040(self.functionUp, self.functionDown, self.functionEnter)
        ky040.start()

        self.resetCounter()

        x = threading.Thread(target=self.watchdog, args=(3,))
        x.start()

        # Show existing data
        self.refreshAllData()



    def getIpAddresses(self):
        ret = {}
        for interface, snics in psutil.net_if_addrs().items():
            ret[interface] = {}
            for snic in snics:
                if snic.family == socket.AF_INET:
                    ret[interface]["ip"] = snic.address
                elif snic.family == socket.AF_PACKET:
                    ret[interface]["mac"] = snic.address
        return ret



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
                time.sleep(0.5)
#            showMenu(self.rootMenu)
