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
