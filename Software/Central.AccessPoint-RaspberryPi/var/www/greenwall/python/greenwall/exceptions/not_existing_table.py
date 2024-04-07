import sys

class NotExistingTable(Exception):
    error_code = 400

    def __init__(self, message, error_code, *args, **kwargs):

        self.traceback = sys.exc_info()

        self.error_code = error_code

        try:
            self.message = '[{0}] {1}'.format(error_code, message.format(*args, **kwargs))
        except (IndexError, KeyError):
            self.message = '[{0}] {1}'.format(error_code, message)

        super().__init__(message)
