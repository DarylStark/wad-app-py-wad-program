"""Module with abstract classes for databases."""

from abc import ABC, abstractmethod

from .model import EventData, Session, SessionState, Speaker


class Database(ABC):
    """Abstract class for a database."""

    def __init__(self) -> None:
        """Set empty data object."""
        self._data: EventData = EventData(sessions=[], speakers=[])

    def get_sessions(self) -> list[Session]:
        """Retrieve the sessions from the database."""
        return self._data.sessions

    def get_speakers(self) -> list[Speaker]:
        """Retrieve the speakers from the database."""
        return self._data.speakers

    def _sync_sessions(self, sessions: list[Session]) -> None:
        sessions_with_id: dict[int, Session] = {
            session.id: session for session in self._data.sessions
        }
        incoming_sessions_with_id: dict[int, Session] = {
            session.id: session for session in sessions
        }
        for id, session in incoming_sessions_with_id.items():
            if id in sessions_with_id:
                sessions_with_id[id] = session
                session.state = SessionState.ACTIVE
            else:
                sessions_with_id[id] = session
                session.state = SessionState.NEW
        for id, session in sessions_with_id.items():
            if id not in incoming_sessions_with_id:
                session.state = SessionState.REMOVED

        # Update the sessions
        self._data.sessions = list(sessions_with_id.values())

    def _update_speaker_list(self) -> None:
        speakers: dict[str, Speaker] = {}
        self._data.speakers = []
        for session in self._data.sessions:
            for speaker in session.speakers:
                obj = speakers.setdefault(speaker.name, speaker)
                obj.sessions.append(session)
        self._data.speakers = list(speakers.values())

    def sync(self, event_data: EventData) -> None:
        """Sync the given event data with the current event data."""
        self._sync_sessions(event_data.sessions)
        self._update_speaker_list()

    @abstractmethod
    def load(self) -> None:
        """Load the data from the database into memory."""

    @abstractmethod
    def save(self) -> None:
        """Save the data to the databae."""
