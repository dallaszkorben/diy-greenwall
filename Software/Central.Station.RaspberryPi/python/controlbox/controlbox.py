from lcddriver.lcddriver import lcd as Lcd
from ky040.ky040 import KY040
from lcdmenu.lcdmenu import LcdMenu

class Controlbox:

    def __init__(self, web_gadget):

        self.web_gadget = web_gadget

        lcd = Lcd()
        maxLine = 2

        self.rootMenu=LcdMenu(lcd, maxLine, self.rootText)

        menu1 = LcdMenu(lcd, maxLine, self.menu1Text)
        menu2 = LcdMenu(lcd, maxLine, self.menu2Text)
        menu3 = LcdMenu(lcd, maxLine, self.menu3Text)
        menu4 = LcdMenu(lcd, maxLine, self.menu4Text)
        menu5 = LcdMenu(lcd, maxLine, self.menu5Text)

        self.rootMenu.addLcdMenu(menu1)
        self.rootMenu.addLcdMenu(menu2)
        self.rootMenu.addLcdMenu(menu3)
        self.rootMenu.addLcdMenu(menu4)
        self.rootMenu.addLcdMenu(menu5)

        self.rootMenu.initialize()

        self.rootMenu.showMenu()

        ky040 = KY040(self.functionUp, self.functionDown, self.functionEnter)
        ky040.start()

    def functionUp(self):
        self.rootMenu.up()

    def functionDown(self):
        self.rootMenu.down()

    def functionEnter(self):
        print("Enter")

    def rootText(self):
        "."

    def menu1Text(self):
        return "menu 1"

    def menu2Text(self):
        return "menu 2"

    def menu3Text(self):
        return "menu 3"

    def menu4Text(self):
        return "menu 4"

    def menu5Text(self):
        return "menu 5"

