"""Module with the WadProgramApp class."""

from collections.abc import Callable

from .database import Database
from .database_specifications import SessionSpecification, TopicSpecification
from .model import Session, Topic
from .program_retriever import ProgramRetriever


class WadProgramApp:
    """Main class for the program.

    Contains all methods for the program.
    """

    def __init__(
        self, retriever: ProgramRetriever, database: Database
    ) -> None:
        """Set correct objects for the class."""
        self._retriever = retriever
        self._database: Database = database
        self._database.load()

    def update_database(
        self,
        *,
        hook_retrieve_total: Callable[[int], None] | None = None,
        hook_retrieve_progress: Callable[[int], None] | None = None,
        hook_sync_total: Callable[[int], None] | None = None,
        hook_sync_progress: Callable[[int], None] | None = None,
        hook_speaker_list_total: Callable[[int], None] | None = None,
        hook_speaker_list_progress: Callable[[int], None] | None = None,
    ) -> None:
        """Update the database."""
        data = self._retriever.retrieve_program(
            hook_total=hook_retrieve_total,
            hook_progress=hook_retrieve_progress,
        )
        self._database.sync(
            data,
            hook_sync_total=hook_sync_total,
            hook_sync_progress=hook_sync_progress,
            hook_speaker_list_total=hook_speaker_list_total,
            hook_speaker_list_progress=hook_speaker_list_progress,
        )
        self._database.save()

    def save_database(self) -> None:
        """Save the database."""
        self._database.save()

    def get_sessions(
        self, spec: SessionSpecification | None = None
    ) -> list[Session]:
        """Retrieve sessions from the database."""
        return self._database.get_sessions(spec)

    def get_topics(self, spec: TopicSpecification) -> list[Topic]:
        """Retrieve sessions from the database."""
        return self._database.get_topics(spec)
