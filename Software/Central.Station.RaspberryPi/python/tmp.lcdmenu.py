#from rpi_lcd import LCD
from lcddriver.lcddriver import lcd as Lcd

class LcdMenu:

    def __init__(self, lcd, maxLine, textFunction, *args):
        self.textFunction = textFunction
        self.args = args

        self.menuList = []
        self.lcd = lcd
        self.maxLine = maxLine

        self.activeMenu = None
        self.startRelativeWindow = None

    def showMenu(self):
        if self.activeMenu:

            activeIndex = self.menuList.index(self.activeMenu)

            self.lcd.clear()

            dispPos = 1
            for i in range(activeIndex + self.startRelativeWindow, activeIndex + self.startRelativeWindow + self.maxLine):

                menu = self.menuList[i]
                value = menu.textFunction(*menu.args)
#                self.lcd.text("> {0}".format(value), dispPos)
                self.lcd.display_string("{0}".format(value), dispPos)

#                if self.activeMenu == menu:
#                    print("> {0}".format(value))
##                    self.lcd.text("> {0}".format(value), dispPos)
#                    self.lcd.display_string(">{0}".format(value), dispPos)
#                else:
#                    print(value)
##                    self.lcd.text("{0}".format(value), dispPos)
#                    self.lcd.display_string("{0}".format(value), dispPos)

                dispPos += 1
#            for menu in self.menuList:
#                value = menu.textFunction(*menu.args)
#                if self.activeMenu == menu:
#                    print("> {0}".format(value))
#                else:
#                    print(value)


#            print("active:", abs(self.startRelativeWindow))
            self.lcd.cursorActiveLine(abs(self.startRelativeWindow) + 1)

            return True

        else:
            for menu in self.menuList:
                result = menu.showMenu()
                if result:
                    return True

            return False

    def initialize(self):
        self.activeMenu = self.menuList[0]
        self.startRelativeWindow = 0

    def addLcdMenu(self, lcdMenu):
        self.menuList.append(lcdMenu)

    def down(self):
        if self.activeMenu:
            if self.activeMenu != self.menuList[-1]:
                activeIndex = self.menuList.index(self.activeMenu)
                self.activeMenu = self.menuList[activeIndex + 1]
                self.startRelativeWindow = max( -(self.maxLine - 1), self.startRelativeWindow - 1)
                self.showMenu()
        else:
            for menu in self.menuList:
                result = menu.down()
                if result:
                    return True
            return False

    def up(self):
        if self.activeMenu:
            if self.activeMenu != self.menuList[0]:
                activeIndex = self.menuList.index(self.activeMenu)
                self.activeMenu = self.menuList[activeIndex - 1]
                self.startRelativeWindow = min( 0, self.startRelativeWindow + 1)
                self.showMenu()
        else:
            for menu in self.menuList:
                result = menu.up()
                if result:
                    return True
            return False

class Test:

    def __init__(self):

        #lcd = LCD()
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

#        print("---")

#        rootMenu.down()

#        print("---")


        from ky040.ky040 import KY040
        ky040 = KY040(self.functionUp, self.functionDown, self.functionEnter)
        ky040.start()


    def functionUp(self):
        self.rootMenu.up()
        print("Up")

    def functionDown(self):
        self.rootMenu.down()
        print("Down")

    def functionEnter(self):
        print("Enter")

    def rootText(self):
        "."

    def menu1Text(self):
        return "menu 1 which is very long so not fitting to the screen"

    def menu2Text(self):
        return "menu 2"

    def menu3Text(self):
        return "menu 3"

    def menu4Text(self):
        return "menu 4"

    def menu5Text(self):
        return "menu 5"


import time
test=Test()
while True:

    time.sleep(0.5)


#lcd.text("Hello,", 1)
#lcd.text("Raspberry Pi!", 2)
