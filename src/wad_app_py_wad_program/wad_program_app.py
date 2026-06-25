from .database import Database
from .program_retriever import ProgramRetriever


class WadProgramApp:
    """Main class for the program."""

    def __init__(
        self, retriever: ProgramRetriever, database: Database
    ) -> None:
        self._retriever = retriever
        self._database: Database = database

    def update_database(self) -> None:
        """Update the database."""
        data = self._retriever.retrieve_program()
