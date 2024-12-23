
#from greenwall.lcddriver.lcddriver import lcd as Lcd
from greenwall.ky040.ky040 import KY040
from greenwall.lcdmenu.lcdmenu import LcdSubMenu, LcdSubElement, LcdRootMenu
from greenwall.lcdmenu.lcdmenu import *

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
        self.piMenu = LcdSubMenu( "PI Box" )
        self.rootMenu.addLcdMenu(self.dataMenu)
        self.rootMenu.addLcdMenu(self.controlMenu)
        self.rootMenu.addLcdMenu(self.alertMenu)
        self.rootMenu.addLcdMenu(self.piMenu)

# ------ Control -------

        controlMenu_pump = LcdSubMenu( " Pump" )
        self.controlMenu.addLcdMenu(controlMenu_pump)

        controlMenu_lamp = LcdSubMenu( " Lamp" )
        self.controlMenu.addLcdMenu(controlMenu_lamp)

# ------ Lamp -------

        lampMenu_on_5sec = LcdSubElement( " Lamp On 5 sec", self.turnLampOn5sec )
        controlMenu_lamp.addLcdMenu(lampMenu_on_5sec)

        lampMenu_on_10sec = LcdSubElement( " Lamp On 30 sec", self.turnLampOn30sec )
        controlMenu_lamp.addLcdMenu(lampMenu_on_10sec)

        lampMenu_off_5sec = LcdSubElement( " Lamp Off 5 sec", self.turnLampOff5sec )
        controlMenu_lamp.addLcdMenu(lampMenu_off_5sec)

        lampMenu_off_10sec = LcdSubElement( " Lamp Off 30 sec", self.turnLampOff30sec )
        controlMenu_lamp.addLcdMenu(lampMenu_off_10sec)

# ------ Pump -------

        pumpMenu_on_5sec = LcdSubElement( " Pump On 5 sec", self.turnPumpOn5sec )
        controlMenu_pump.addLcdMenu(pumpMenu_on_5sec)

        pumpMenu_on_30sec = LcdSubElement( " Pump On 30 sec", self.turnPumpOn30sec )
        controlMenu_pump.addLcdMenu(pumpMenu_on_30sec)

        pumpMenu_on_60sec = LcdSubElement( " Pump On 60 sec", self.turnPumpOn60sec )
        controlMenu_pump.addLcdMenu(pumpMenu_on_60sec)

        pumpMenu_on_120sec = LcdSubElement( " Pump On 120 sec", self.turnPumpOn120sec )
        controlMenu_pump.addLcdMenu(pumpMenu_on_120sec)

        pumpMenu_off = LcdSubElement( " Pump Off", self.turnPumpOff )
        controlMenu_pump.addLcdMenu(pumpMenu_off)

# ------ PI Box menu -------

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
            pressureMenu =    LcdSubElement("pres: ")
            dateMenu =        LcdSubElement("date: ")
            ipMenu =          LcdSubElement("ip:   ")

            stationMenu.addLcdMenu(levelMenu)
            stationMenu.addLcdMenu(temperatureMenu)
            stationMenu.addLcdMenu(humidityMenu)
            stationMenu.addLcdMenu(pressureMenu)
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
            pressureValue = i['pressureValue']

            dateString = datetime.fromtimestamp(timeStamp).astimezone().isoformat()

            stationMenu = self.getStationMenu(si)

            # water level
            stationMenu.menuList[1].setText("levl: {0} mm".format(levelValue))

            # temperature
            stationMenu.menuList[2].setText("temp: {0} {1}C".format(temperatureValue, chr(223)))

            # humidity
            stationMenu.menuList[3].setText("relh: {0} %".format(humidityValue))

            # pressure
            stationMenu.menuList[4].setText("press: {0} Pa".format(pressureValue))
            stationMenu.menuList[4].setRotateAt(7)

            # date
            stationMenu.menuList[5].setText("date: {0}".format(dateString))
            stationMenu.menuList[5].setRotateAt(6)

            # ip
            stationMenu.menuList[6].setText("ip: {0}".format(ip))
            stationMenu.menuList[6].setRotateAt(4)

            if stationMenu.activeMenu and not stationMenu.startRelativeWindow == None:
#                stationMenu.showMenu()
                showMenu(stationMenu)

    def refreshData(self, stationId):
        latestValues = self.webGadget.reportSensor.getLatestValues(stationId)
        self.refreshLatestValues(latestValues)

    def refreshAllData(self):
        latestValues = self.webGadget.reportSensor.getLatestValues()
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




    def turnLampOn5sec(self):
        self.webGadget.lamp.turnLampOn(5)

    def turnLampOn10sec(self):
        self.webGadget.lamp.turnLampOn(10)

    def turnLampOn30sec(self):
        self.webGadget.lamp.turnLampOn(30)

    def turnLampOff5sec(self):
        self.webGadget.lamp.turnLampOff(5)

    def turnLampOff10sec(self):
        self.webGadget.lamp.turnLampOff(10)

    def turnLampOff30sec(self):
        self.webGadget.lamp.turnLampOff(30)

# ---

    def turnPumpOn5sec(self):
        self.webGadget.pump.turnPumpOn(5)

    def turnPumpOn10sec(self):
        self.webGadget.pump.turnPumpOn(10)

    def turnPumpOn30sec(self):
        self.webGadget.pump.turnPumpOn(30)

    def turnPumpOn60sec(self):
        self.webGadget.pump.turnPumpOn(60)

    def turnPumpOn120sec(self):
        self.webGadget.pump.turnPumpOn(120)

    def turnPumpOff(self):
        self.webGadget.pump.turnPumpOff()

