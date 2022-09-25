import inspect
from abc import abstractmethod

class EP:

    CODE_OK = 200
    CODE_CREATED = 201
    CODE_BAD_REQUEST = 400
    CODE_INTERNAL_SERVER_ERROR = 500

    def executeByParameters(*args):
        raise NotImplementedError(f"{inspect.currentframe().f_code.co_name}() is not implemented")

    def executeByPayload(*args):
        raise NotImplementedError(f"{inspect.currentframe().f_code.co_name}() is not implemented")

    def getRequestDescriptionWithPayloadParameters(self) -> dict:
        raise NotImplementedError(f"{inspect.currentframe().f_code.co_name}() is not implemented")

