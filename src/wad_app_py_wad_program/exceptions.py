"""Module with package local exceptions."""


class WadProgramException(BaseException):
    """Base exception for WadProgram."""

    pass


class PageNotFoundException(WadProgramException):
    """Exception for when a specific page is not found."""

    pass
