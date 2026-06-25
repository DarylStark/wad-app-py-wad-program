"""Module with a abstract class for ProgramRetrievers."""

from abc import ABC, abstractmethod

from .model import EventData


class ProgramRetriever(ABC):
    """Abstrat class for program retrievers."""

    @abstractmethod
    def retrieve_program(self) -> EventData:
        """Abstract method to retrieve the program."""
