
class UserCreationFailedError(Exception):
    """Exception raised when a user creation fails for some reason."""
    def __init__(self, message="User creation failed."):
        self.message = message
        super().__init__(self.message)

class ServerError(Exception):
    """Exception raised when a server error occurs."""
    def __init__(self, message="Server error."):
        self.message = message
        super().__init__(self.message)

class BadRequestError(Exception):
    """Exception raised when a bad request is made."""
    def __init__(self, message="Bad request."):
        self.message = message
        super().__init__(self.message)