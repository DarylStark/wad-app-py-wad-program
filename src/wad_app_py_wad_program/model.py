"""The data model for the package."""

from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from enum import Enum

from pydantic import BaseModel, Field


class ModelVisitor(ABC):
    """Vistor for the model."""

    @abstractmethod
    def visit_session(self, session: Session) -> None:
        """Visistor for a session."""

    @abstractmethod
    def visit_topic(self, topic: Topic) -> None:
        """Visistor for a topic."""

    @abstractmethod
    def done(self) -> None:
        """When done with the visitor."""


class SessionState(Enum):
    """The state for a session.

    NEW: the session was not seen by the user yet.
    ACTIVE: the session was seen by the user.
    REMOVED: the sessions was once in the schedule but not anymore.
    """

    NEW = 'new'
    ACTIVE = 'active'
    REMOVED = 'removed'


class InterestLevel(Enum):
    """The interest for a session.

    UNSPECIFIED: nothing specified yet.
    NOT_INTERESTED: not interested in the session.
    WATCH_LATER: watch after the conference on YouTube.
    INTERESTED: want to watch this sessions.
    ALTERNATIVE: might watch it if time is available.
    """

    UNSPECIFIED = 'unspecified'
    NOT_INTERESTED = 'not_interested'
    WATCH_LATER = 'watch_later'
    INTERESTED = 'interested'
    ALTERNATIVE = 'alternative'


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
    start_time: datetime | None = None
    end_time: datetime | None = None
    topics: list[str] = Field(default_factory=list)
    speakers: list[Speaker] = Field(default_factory=list)
    state: SessionState = SessionState.ACTIVE
    interest_level: InterestLevel = InterestLevel.UNSPECIFIED

    def accept(self, visitor: ModelVisitor) -> None:
        """Accept a visitor.

        Can be used to implement Session specific behavior
        """
        visitor.visit_session(self)

    @property
    def duration(self) -> timedelta:
        """Return the duration of the sessions."""
        if self.end_time and self.start_time:
            return self.end_time - self.start_time
        return timedelta()

    @property
    def day(self) -> Day:
        """Return the Day object for this model."""
        if not self.start_time:
            return Day.WED
        return Day(self.start_time.strftime('%a').lower())


class Speaker(BaseModel):
    """Model for a Speaker."""

    name: str
    job: str
    tagline: str
    summary: str
    sessions: list[Session] = Field(default_factory=list)


class Topic(BaseModel):
    """Model for a Topic."""

    name: str
    is_main_topic: bool = False

    def accept(self, visitor: ModelVisitor) -> None:
        """Accept a visitor.

        Can be used to implement Topic specific behavior
        """
        visitor.visit_topic(self)


class EventData(BaseModel):
    """Model for a the complete event data.

    Contains all sessions and all speakers.
    """

    sessions: list[Session]
    speakers: list[Speaker] = Field(default_factory=list)
    topics: list[Topic] = Field(default_factory=list)
