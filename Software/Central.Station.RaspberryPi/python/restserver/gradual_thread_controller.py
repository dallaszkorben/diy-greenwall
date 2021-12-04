import logging

class GradualThreadController(object):
    __instance = None

    def __new__(cls):
        if GradualThreadController.__instance is None:
            GradualThreadController.__instance = object.__new__(cls)
            #GradualThreadController.__instance.__init__() 
        return GradualThreadController.__instance

    @classmethod
    def getInstance(cls):
        inst = cls.__new__(cls)
        cls.__init__(cls.__instance) 
        return inst

    def __init__(self):
        self.shouldStop = False
        self.running = False
        self.threadId = None

    def run(self, threadId):
        logging.debug( "Set Thread Started >")

        self.threadId = threadId
        self.shouldStop = False
        self.running = True

    def isRunning(self):
        return self.running

    def getStatus(self):
        return {"inProgress": self.running, "id": self.threadId}

    def stopRunning(self):
        self.running = False
        self.shouldStop = False
        self.threadId = None

        logging.debug( "Set Thread Stopped <")

    def shouldItStop(self):
        return self.shouldStop
 
    def indicateToStop(self):
        self.shouldStop = True

