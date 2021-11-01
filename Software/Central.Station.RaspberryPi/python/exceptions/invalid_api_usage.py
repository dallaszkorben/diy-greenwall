import sys

class InvalidAPIUsage(Exception):
    error_code = 400

    def __init__(self, message, error_code, *args, **kwargs):
#        super().__init__(message)
#        self.message = message
#        if status_code is not None:
#            self.status_code = status_code
#            self.code = status_code
#        self.payload = payload

        self.traceback = sys.exc_info()

        self.error_code = error_code

        try:
            msg = '[{0}] {1}'.format(error_code, message.format(*args, **kwargs))
        except (IndexError, KeyError):
            msg = '[{0}] {1}'.format(error_code, message)

        super().__init__(msg)
