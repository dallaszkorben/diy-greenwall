
from lcddriver.lcddriver import lcd as Lcd
import threading

cursorMap = [ 
    0b01000, 
    0b01100, 
    0b01110, 
    0b01111, 
    0b01110, 
    0b01100, 
    0b01000, 
    0b00000
]

backMap = [ 
    0b00100, 
    0b01110, 
    0b10101, 
    0b00100, 
    0b00100, 
    0b00100, 
    0b00111, 
    0b00000
]

hideMap = [ 
    0b00100, 
    0b01010, 
    0b10001, 
    0b10101, 
    0b10001, 
    0b01010, 
    0b00100, 
    0b00000
]

customCharacterCollection = [
    cursorMap,
    backMap,
    hideMap,
]


maxMenuLines = 2
lcd = Lcd()
lcd.loadCustomChars(customCharacterCollection)

lock = threading.Lock()

ASCII_CURSOR = 0
ASCII_BACK = 1
ASCII_HIDE = 2

def showMenu(menu, shift=0, clear=True):

    with lock:
        menu.showMenu(shift=shift, clear=clear)

class AbstractLcdMenu:

    def __init__(self):

        self.menuList = []

        self.text = None
        self.rotateAt = 0

        self.activeMenu = None
        self.startRelativeWindow = None

        self.parent = None

        self.executeFunction = None


    def setText(self, text):
        self.text = text

    def setRotateAt(self, rotateAt):
        self.rotateAt = rotateAt

    def setExecuteFunction(self, executeFunction):
        self.executeFunction = executeFunction

    def showMenu(self, shift=0, clear=True):

        if not lcd.screenOn:
            return

        visibleLength = 15

        if self.activeMenu:

            activeIndex = self.menuList.index(self.activeMenu)

            if clear:
                lcd.clear()

            wasShift = False

            dispPos = 1
            for i in range(activeIndex + self.startRelativeWindow, activeIndex + self.startRelativeWindow + min(maxMenuLines, len(self.menuList))):

                subMenu = self.menuList[i]

                needToShift = shift > 0 and len(subMenu.text) > visibleLength and i == activeIndex
                if needToShift:
                    fixPart = subMenu.text[0:subMenu.rotateAt]
                    rotatingPart = subMenu.text[subMenu.rotateAt:]

                    shift = shift % len(rotatingPart)
                    end = shift + visibleLength - len(fixPart)
                    text = fixPart + (rotatingPart + " " + rotatingPart)[shift:end]

                else:
                    text = subMenu.text

                text = text[0:visibleLength]

                if activeIndex == i:
                    text = chr(ASCII_CURSOR) + text
                else:
                    text = " " + text

                if shift==0 or (activeIndex == i and ((isinstance(subMenu, LcdSubMenu)) or isinstance(subMenu, LcdSubElement))):
                    lcd.display_string("{0}".format(text), dispPos)

                dispPos += 1

#               lcd.cursorActiveLine(abs(self.startRelativeWindow) + 1)

            return True

        else:
            for subMenu in self.menuList:
                result = subMenu.showMenu(shift, clear)
                if result:
                    return True

            return False

    def initialize(self):

        if len(self.menuList) == 1:
            self.activeMenu = self.menuList[0]
            self.startRelativeWindow = 0

        elif len(self.menuList) <= maxMenuLines:
            self.activeMenu = self.menuList[1]
            self.startRelativeWindow = -1
        else:
            self.activeMenu = self.menuList[1]
            self.startRelativeWindow = 0

    def setParent(self, parent):
        self.parent = parent

    def addLcdMenu(self, lcdMenu):
        self.menuList.append(lcdMenu)
        lcdMenu.setParent(self)

    def down(self):
        if not lcd.screenOn:
            lcd.setScreenOn()

        if self.activeMenu:
            if self.activeMenu != self.menuList[-1]:

                activeIndex = self.menuList.index(self.activeMenu)
                self.activeMenu = self.menuList[activeIndex + 1]
                self.startRelativeWindow = max( -(maxMenuLines - 1), self.startRelativeWindow - 1)

#                self.showMenu()
                showMenu(self)

                return True
        else:
            for menu in self.menuList:
                result = menu.down()
                if result:
                    return True
            return False

    def up(self):
        if not lcd.screenOn:
            lcd.setScreenOn()

        if self.activeMenu:
            if self.activeMenu != self.menuList[0]:
                activeIndex = self.menuList.index(self.activeMenu)
                self.activeMenu = self.menuList[activeIndex - 1]
                self.startRelativeWindow = min( 0, self.startRelativeWindow + 1)

#                self.showMenu()
                showMenu(self)

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

                showMenu(self.parent)

            # if there is no executeFunction then jump in
            elif isinstance(self.activeMenu, LcdSubMenu) and not self.activeMenu.executeFunction:

                # and hand it over to the active menu
                self.activeMenu.initialize()

                self.previousActiveMenu = self.activeMenu
                self.previousRelativeWindow = self.startRelativeWindow

                # clear activation in this menu
                self.activeMenu = None
                self.startRelativeWindow = None

#                self.showMenu()
                showMenu(self)

            # if there is executeFunction then execute
            elif self.activeMenu.executeFunction: 

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

    def isIn(self, menu):
        if menu.activeMenu and not menu.startRelativeWindow == None:
            return True
        else:
            for subMenu in menu.menuList:
                result = self.isIn(subMenu)
                if result:
                    return True
            return False

    def removeSubMenu(self, subMenu):

        # remove this menu
        self.menuList.remove(subMenu)

        # if we are in the subMenu (in any level)
        if self.isIn(subMenu):

            # move up to the parent
            subMenu.parent.initialize()
            showMenu(subMenu.parent)

        elif subMenu.parent.activeMenu and not subMenu.parent.startRelativeWindow == None:

            subMenu.parent.initialize()
            showMenu(subMenu.parent)

class LcdRootMenu(AbstractLcdMenu):

    def __init__(self):

        super().__init__()
        self.setText("_")

#        screenOffMenu = LcdSubMenu(".")
        screenOffMenu = LcdSubMenu(chr(ASCII_HIDE))
#        screenOffMenu.executeFunction = lcd.backlightOff
        screenOffMenu.executeFunction = self.swapBackLight
        self.addLcdMenu(screenOffMenu)

    def swapBackLight(self):
        if not lcd.screenOn:
            lcd.setScreenOn()
        else:
            lcd.setScreenOff()

class LcdSubMenu(AbstractLcdMenu):

    def __init__(self, text, rotateAt=0):

        super().__init__()
        self.setText( text )
        self.setRotateAt( rotateAt )

#        backMenu = LcdBackMenu("^")
        backMenu = LcdBackMenu(chr(ASCII_BACK))
        self.addLcdMenu(backMenu)

class LcdSubElement(AbstractLcdMenu):

    def __init__(self, text, executeFunction=None, rotateAt=0):

        super().__init__()
        self.setText( text )
        self.setExecuteFunction(executeFunction)
        self.setRotateAt( rotateAt )

class LcdBackMenu(AbstractLcdMenu):

    def __init__(self, text):

        super().__init__()
        self.setText( text )

