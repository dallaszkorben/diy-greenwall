from lcddriver.lcddriver import lcd as Lcd
from ky040.ky040 import KY040
from lcdmenu.lcdmenu import LcdSubMenu, LcdSubElement, LcdRootMenu
import time
from datetime import datetime
import threading

class Controlbox:

    def __init__(self, web_gadget):

        self.webGadget = web_gadget

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


#

        self.rootMenu.initialize()

        self.rootMenu.showMenu()

        ky040 = KY040(self.functionUp, self.functionDown, self.functionEnter)
        ky040.start()

        x = threading.Thread(target=self.refreshAllData)
        x.start()

    def functionUp(self):
        self.rootMenu.up()
#        self.rootMenu.showMenu()

    def functionDown(self):
        self.rootMenu.down()
#        self.rootMenu.showMenu()

    def functionEnter(self):
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
                self.dataMenu.showMenu()


        return stationMenu

    def refreshAllData(self):

        while True:

            time.sleep(10)

            latestValues = self.webGadget.report.getLatestValues()

            # go through the latestValues list
            for i in latestValues:
                stationId = i["stationId"]
                ip = i["ip"]
                timeStamp = i['timeStamp']
                levelValue = i['levelValue']
                temperatureValue = i['temperatureValue']
                humidityValue = i['humidityValue']

                dateString = datetime.fromtimestamp(timeStamp).astimezone().isoformat()

                stationMenu = self.getStationMenu(stationId)

                # water level
                stationMenu.menuList[1].text = "levl: {0} mm".format(levelValue)

                # temperature
                stationMenu.menuList[2].text = "temp: {0} {1}C".format(temperatureValue, chr(223))

                # humidity
                stationMenu.menuList[3].text = "relh: {0} %".format(humidityValue)

                # date
                stationMenu.menuList[4].text = "date: {0} %".format(dateString)

                # ip
                stationMenu.menuList[5].text = "ip: {0} %".format(ip)

                if stationMenu.activeMenu and not stationMenu.startRelativeWindow == None:
                    stationMenu.showMenu()


    def rrrrefreshActualData(self):

        loop = 0
        while True:

            loop += 1
            time.sleep(10)

            START = 1
            for index, subMenu in enumerate(self.dataMenu.menuList[START:], START):
                print(subMenu.text)


                # water level
                subMenu.menuList[1].text = "  h:  {0} mm".format(loop)

                # temperature
                subMenu.menuList[2].text = "  t:  {0} {1}C".format(loop, chr(223))

                # humidity
                subMenu.menuList[3].text = "  rh: {0} %".format(loop)

                if subMenu.activeMenu and not subMenu.startRelativeWindow == None:
                    subMenu.showMenu()

                #self.subMenu1.removeSubMenu(subMenu)

#                time.sleep(20)

#            break
#            time.sleep(10)
