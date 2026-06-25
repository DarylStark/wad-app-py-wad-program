"""The data model for the package."""

from pydantic import BaseModel, Field


class Session(BaseModel):
    """Model for a Session."""

    title: str
    speakers: list[Speaker] = Field(default_factory=list)


class Speaker(BaseModel):
    """Model for a Speaker."""

    name: str
    sessions: list[Session] = Field(default_factory=list)


class EventData(BaseModel):
    """Model for a the complete event data.

    Contains all sessions and all speakers.
    """

    sessions: list[Session]
    speakers: list[Speaker]
