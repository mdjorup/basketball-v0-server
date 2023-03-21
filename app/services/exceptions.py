
class UserCreationFailedError(Exception):
    """Exception raised when a user creation fails for some reason."""
    def __init__(self, message="User creation failed."):
        self.message = message
        super().__init__(self.message)