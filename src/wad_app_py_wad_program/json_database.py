from typing import override

from .database import Database
from .model import EventData


class JsonDatabase(Database):
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
