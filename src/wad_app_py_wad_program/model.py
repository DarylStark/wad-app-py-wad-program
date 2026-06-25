"""The data model for the package."""

from datetime import date, datetime

from pydantic import BaseModel, Field
from enum import Enum


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


class Session(BaseModel):
    """Model for a Session."""

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
