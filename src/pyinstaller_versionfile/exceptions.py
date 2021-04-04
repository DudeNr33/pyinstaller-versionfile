"""
Exception classes for pyinstaller-versionfile.
"""

class InputError(Exception):
    """
    The given metadata input file is not as expected.
    """


class UsageError(Exception):
    """
    Exception for all cases where the end user is giving wrong inputs to the program.
    """


class ValidationError(Exception):
    """
    Input data is not valid.
    """


class InternalUsageError(Exception):
    """
    Intended to be used in places where the error is not caused by the end user, but by a programming error.
    """

    MESSAGE_PREFIX = """Looks like you encountered an internal programming error!
    Please file a bug report at: https://github.com/DudeNr33/pyinstaller-versionfile
    
    Please include the following error message and a description how to reproduce the problem:
    
    """

    def __init__(self, message):
        super(InternalUsageError, self).__init__(self.MESSAGE_PREFIX + message)  # pylint: disable=super-with-arguments
