from lcddriver.lcddriver import lcd as Lcd

maxMenuLines = 2
lcd = Lcd()


class AbstractLcdMenu:

    def __init__(self):

        self.menuList = []

        self.text = None

        self.activeMenu = None
        self.startRelativeWindow = None

        self.parent = None

        self.executeFunction = None

    def setText(self, text):
        self.text = text

    def setExecuteFunction(self, executeFunction):
        self.executeFunction = executeFunction

    def showMenu(self):
        if self.activeMenu:

            activeIndex = self.menuList.index(self.activeMenu)

            lcd.clear()

            dispPos = 1
            for i in range(activeIndex + self.startRelativeWindow, activeIndex + self.startRelativeWindow + min(maxMenuLines, len(self.menuList))):

                subMenu = self.menuList[i]
                text = subMenu.text
                lcd.display_string("{0}".format(text), dispPos)

                dispPos += 1

            lcd.cursorActiveLine(abs(self.startRelativeWindow) + 1)

            return True

        else:
            for subMenu in self.menuList:
                result = subMenu.showMenu()
                if result:
                    return True

            return False

    def initialize(self):
        self.activeMenu = self.menuList[1]
        self.startRelativeWindow = 0

    def setParent(self, parent):
        self.parent = parent

    def addLcdMenu(self, lcdMenu):
        self.menuList.append(lcdMenu)
        lcdMenu.setParent(self)

    def down(self):
        if self.activeMenu:
            if self.activeMenu != self.menuList[-1]:

                activeIndex = self.menuList.index(self.activeMenu)
                self.activeMenu = self.menuList[activeIndex + 1]
                self.startRelativeWindow = max( -(maxMenuLines - 1), self.startRelativeWindow - 1)

                self.showMenu()

                return True
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

                return True
        else:

            for menu in self.menuList:
                result = menu.up()
                if result:
                    return True
            return False

    def enter(self):
        if self.activeMenu:

            # if back
            if isinstance(self.activeMenu, LcdBackMenu):
                self.activeMenu = None
                self.startRelativeWindow = None

                self.parent.activeMenu = self.parent.previousActiveMenu
                self.parent.startRelativeWindow = self.parent.previousRelativeWindow

                self.parent.showMenu()

            # if there is not executeFunction then jump in
            elif isinstance(self.activeMenu, LcdSubMenu) and not self.activeMenu.executeFunction:

                # and hand it over to the active menu
                self.activeMenu.activeMenu = self.activeMenu.menuList[1]
                self.activeMenu.startRelativeWindow = 0

                self.previousActiveMenu = self.activeMenu
                self.previousRelativeWindow = self.startRelativeWindow

                # clear activation in this menu
                self.activeMenu = None
                self.startRelativeWindow = None

                self.showMenu()

            # if there is executeFunction then execute
            elif isinstance(self.activeMenu, LcdSubElement) and self.activeMenu.executeFunction:

                self.activeMenu.executeFunction()

            else:
                pass

            return True

        else:

            for menu in self.menuList:
                result = menu.enter()
                if result:
                    return True
            return False


class LcdRootMenu(AbstractLcdMenu):

    def __init__(self):

        super().__init__()
        self.setText("_")

        screenOffMenu = LcdSubMenu(".")
        screenOffMenu.executeFunction = lcd.backlightOff
        self.addLcdMenu(screenOffMenu)

class LcdSubMenu(AbstractLcdMenu):

    def __init__(self, text):

        super().__init__()
        self.setText( text )

        backMenu = LcdBackMenu("^")
        self.addLcdMenu(backMenu)

class LcdSubElement(AbstractLcdMenu):

    def __init__(self, text, executeFunction=None):

        super().__init__()
        self.setText( text )
        self.setExecuteFunction(executeFunction)

class LcdBackMenu(AbstractLcdMenu):

    def __init__(self, text):

        super().__init__()
        self.setText( text )

