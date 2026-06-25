"""Module with a Json implementation for the database."""

from typing import override

from .database import Database
from .model import EventData


class JsonDatabase(Database):
    """Json implementation for the database.

    This class is constructed with a filename to a Json file. That file will
    be used to store the database.
    """

    def __init__(self, json_filename: str) -> None:
        """Set values for the object."""
        self._filename = json_filename

    @override
    def get_sessions(self) -> EventData:
        """Retrieve the sessions from the database."""
        return EventData(sessions=[], speakers=[])

    @override
    def save_sessions(self, data: EventData) -> None:
        """Save all sessions to the databae."""
