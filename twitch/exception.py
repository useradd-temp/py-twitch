class BaseError(Exception):
    def __init__(self, message, code=None, params=None):
        self.message = message
        self.code = code
        self.params = params
        self.error_list = [self]
        super().__init__(message, code, params)

    def __iter__(self):
        for error in self.error_list:
            message = error.message
            if error.params:
                message %= error.params
            yield str(message)

    def __str__(self):
        return repr(list(self))

    def __repr__(self):
        return f"ValidationError({self})"


class APIError(BaseError):
    pass


class NotProvideError(BaseError):
    pass


class ValidationError(BaseError):
    pass
