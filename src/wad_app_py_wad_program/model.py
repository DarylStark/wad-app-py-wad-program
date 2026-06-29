"""The data model for the package."""

from abc import ABC, abstractmethod
from datetime import date, datetime
from enum import Enum

from pydantic import BaseModel, Field


class ModelVisitor(ABC):
    """Vistor for the model."""

    @abstractmethod
    def visit_session(self, session: Session) -> None:
        """Visistor for a session."""

    @abstractmethod
    def done(self) -> None:
        """When done with the visitor."""


class SessionState(Enum):
    """The state for a session.

    NEW: the session was added in the last sync.
    ACTIVE: the session was seen in the last time it synced.
    REMOVED: the session was seen once, but wasn't in there after the last time
        it synced.
    """

    NEW = 'new'
    ACTIVE = 'active'
    REMOVED = 'removed'

class Day(Enum):
    """Specific days.

    Only used by filters.
    """

    WED = 'wed'
    THU = 'thu'
    FRI = 'fri'

    @property
    def iso_day_number(self) -> int:
        """Convert the given date to a ISO number."""
        if self == Day.WED:
            return 3 
        elif self == Day.THU:
            return 4
        return 5


class Session(BaseModel):
    """Model for a Session."""

    url: str
    id: int
    title: str
    main_topic: str
    description: str
    stage: str
    present_date: date | None = None
    start_time: datetime | None = None
    end_time: datetime | None = None
    topics: list[str] = Field(default_factory=list)
    speakers: list[Speaker] = Field(default_factory=list)
    state: SessionState = SessionState.ACTIVE

    def accept(self, visitor: ModelVisitor) -> None:
        """Accept a visitor.

        Can be used to implement Session specific behavior
        """
        visitor.visit_session(self)


class Speaker(BaseModel):
    """Model for a Speaker."""

    name: str
    job: str
    tagline: str
    summary: str
    sessions: list[Session] = Field(default_factory=list)


class EventData(BaseModel):
    """Model for a the complete event data.

    Contains all sessions and all speakers.
    """

    sessions: list[Session]
    speakers: list[Speaker]
