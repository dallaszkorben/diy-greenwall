import inspect
from abc import abstractmethod

class EP:

    def executeByParameters(*args):
        raise NotImplementedError(f"{inspect.currentframe().f_code.co_name}() is not implemented")

    def executeByPayload(*args):
        raise NotImplementedError(f"{inspect.currentframe().f_code.co_name}() is not implemented")

    def getRequestDescriptionWithPayloadParameters(self) -> dict:
        raise NotImplementedError(f"{inspect.currentframe().f_code.co_name}() is not implemented")



