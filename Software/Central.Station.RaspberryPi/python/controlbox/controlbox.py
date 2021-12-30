from lcddriver.lcddriver import lcd as Lcd
from ky040.ky040 import KY040
from lcdmenu.lcdmenu import LcdSubMenu, LcdSubElement, LcdRootMenu
import time
import threading

class Controlbox:

    def __init__(self, web_gadget):

        self.web_gadget = web_gadget

#        lcd = Lcd()
#        maxLine = 2

        self.rootMenu=LcdRootMenu()

        self.subMenu1 = LcdSubMenu( "Show actual data" )
        subMenu2 = LcdSubMenu( "Control actuators" )
        subMenu3 = LcdSubMenu( "Alerts" )
        self.rootMenu.addLcdMenu(self.subMenu1)
        self.rootMenu.addLcdMenu(subMenu2)
        self.rootMenu.addLcdMenu(subMenu3)

# ------ Show actual data -------

        subMenu11 = LcdSubMenu( "Station 10" )
        subMenu12 = LcdSubMenu( "Station 11" )
        subMenu13 = LcdSubMenu( "Station 12" )
        self.subMenu1.addLcdMenu(subMenu11)
        self.subMenu1.addLcdMenu(subMenu12)
        self.subMenu1.addLcdMenu(subMenu13)

#        

        subMenu111 = LcdSubElement("  Level: 35mm")
        subMenu112 = LcdSubElement("  Temp: 23" + chr(223) + "C")
        subMenu113 = LcdSubElement("  Hum: 30%")
        subMenu11.addLcdMenu(subMenu111)
        subMenu11.addLcdMenu(subMenu112)
        subMenu11.addLcdMenu(subMenu113)

        subMenu121 = LcdSubElement("  Level: 32mm")
        subMenu122 = LcdSubElement("  Temp: 22.4" + chr(223) + "C")
        subMenu123 = LcdSubElement("  Hum: 32.3%")
        subMenu12.addLcdMenu(subMenu121)
        subMenu12.addLcdMenu(subMenu122)
        subMenu12.addLcdMenu(subMenu123)

        subMenu131 = LcdSubElement("  Level: 29mm")
        subMenu132 = LcdSubElement("  Temp: 24.5" + chr(223) + "C")
        subMenu133 = LcdSubElement("  Hum: 29.7%")
        subMenu13.addLcdMenu(subMenu131)
        subMenu13.addLcdMenu(subMenu132)
        subMenu13.addLcdMenu(subMenu133)

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

        x = threading.Thread(target=self.refreshActualData)
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


    def refreshActualData(self):

        while True:

            time.sleep(20)

            START = 1
            for index, subMenu in enumerate(self.subMenu1.menuList[START:], START):
                print(subMenu.text)

                self.subMenu1.removeSubMenu(subMenu)

                time.sleep(20)

            break
            time.sleep(10)
