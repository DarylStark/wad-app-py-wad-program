"""Module with a Json implementation for the database."""

from pathlib import Path
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
        super().__init__()
        self._filename = json_filename

    @override
    def load(self) -> None:
        """Load the data from the database into memory."""
        try:
            json_text = Path(self._filename).read_text(encoding='utf-8')
            self._data = EventData.model_validate_json(json_text)
            self._update_speaker_list()
        except FileNotFoundError:
            pass

    @override
    def save(self) -> None:
        """Save the data to the databae."""
        data_to_save = self._data.model_copy(deep=True)
        for session in data_to_save.sessions:
            for speaker in session.speakers:
                speaker.sessions = []
        data_to_save.speakers = []

        Path(self._filename).write_text(
            data_to_save.model_dump_json(),
            encoding='utf-8',
        )
