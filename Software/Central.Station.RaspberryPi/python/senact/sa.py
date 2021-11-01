import inspect
from abc import abstractmethod
from senact.senact import SenAct

class SA:

    def getSenactType(self) -> SenAct:
        raise NotImplementedError(f"{inspect.currentframe().f_code.co_name}() is not implemented")

    def getSenactId(self):
        raise NotImplementedError(f"{inspect.currentframe().f_code.co_name}() is not implemented")

    def configure(self):
        raise NotImplementedError(f"{inspect.currentframe().f_code.co_name}() is not implemented")

    def unconfigure(self):
        raise NotImplementedError(f"{inspect.currentframe().f_code.co_name}() is not implemented")


