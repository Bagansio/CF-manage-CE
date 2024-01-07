class GeneralException(Exception):
    """Base class for general exceptions."""

    def __init__(self, error_code, message):
        super().__init__(message)
        self.error_code = error_code
        self.message = message
        
class ServerException(GeneralException):
    """Base class for Server exceptions."""

    def __init__(self, message):
        super().__init__(500, message)
        
class BadRequestException(GeneralException):
    """Base class for BadRequest exceptions."""

    def __init__(self, message):
        super().__init__(400,message)

        
class ToManyException(GeneralException):
    """Base class for ToMany exceptions."""

    def __init__(self, message):
        super().__init__(429,message)
