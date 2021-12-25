from ky040.ky040 import KY040

class Controlbox:

    def __init__(self, web_gadget):

        self.web_gadget = web_gadget
        ky040 = KY040(self.functionUp, self.functionDown, self.functionEnter)
        ky040.start()


    def functionUp(self):
        print("Up")

    def functionDown(self):
        print("Down")

    def functionEnter(self):
        print("Enter")