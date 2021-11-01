import inspect
from abc import abstractmethod
from senact.senact import SenAct

class EG:

    def getGadgetName(self):
        raise NotImplementedError(f"{inspect.currentframe().f_code.co_name}() is not implemented")

    def getSensor(self, id):
        raise NotImplementedError(f"{inspect.currentframe().f_code.co_name}() is not implemented")

    def getActuator(self, id):
        raise NotImplementedError(f"{inspect.currentframe().f_code.co_name}() is not implemented")

    def getSensorIds(self):
        raise NotImplementedError(f"{inspect.currentframe().f_code.co_name}() is not implemented")

    def getActuatorIds(self):
        raise NotImplementedError(f"{inspect.currentframe().f_code.co_name}() is not implemented")

    def configure(self):
        raise NotImplementedError(f"{inspect.currentframe().f_code.co_name}() is not implemented")

    def unconfigure(self):
        sensorIds = self.getSensorIds()
        for id in sensorIds:
            sensor = self.getSensor(id)
            sensor.unconfigure()

        actuatorIds = self.getActuatorIds()
        for id in actuatorIds:
            actuator = self.getActuator(id)
            actuator.unconfigure()
