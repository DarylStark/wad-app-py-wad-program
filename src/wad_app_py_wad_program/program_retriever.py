"""Module with a abstract class for ProgramRetrievers."""

from abc import ABC, abstractmethod
from collections.abc import Callable

from .model import EventData


class ProgramRetriever(ABC):
    """Abstrat class for program retrievers."""

    @abstractmethod
    def retrieve_program(
        self,
        *,
        hook_total: Callable[[int], None] | None = None,
        hook_progress: Callable[[int], None] | None = None,
    ) -> EventData:
        """Abstract method to retrieve the program."""
