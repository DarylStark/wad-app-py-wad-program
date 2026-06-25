"""Module with the WadProgramApp class."""

from .database import Database
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

    def update_database(self) -> None:
        """Update the database."""
        data = self._retriever.retrieve_program()
