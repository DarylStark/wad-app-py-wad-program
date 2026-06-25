"""Module with abstract classes for databases."""

from abc import ABC, abstractmethod

from .model import EventData


class Database(ABC):
    """Abstract class for a database."""

    @abstractmethod
    def get_sessions(self) -> EventData:
        """Retrieve the sessions from the database."""

    @abstractmethod
    def save_sessions(self, data: EventData) -> None:
        """Save all sessions to the databae."""
