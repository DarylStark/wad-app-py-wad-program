from abc import ABC, abstractmethod

from .model import EventData


class Database(ABC):
    @abstractmethod
    def get_sessions(self) -> EventData:
        """Retrieve the sessions from the database."""

    @abstractmethod
    def save_sessions(self, data: EventData) -> None:
        """Save all sessions to the databae."""
