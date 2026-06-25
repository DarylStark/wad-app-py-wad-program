from pydantic import BaseModel, Field


class Session(BaseModel):
    title: str
    speakers: list[Speaker] = Field(default_factory=list)


class Speaker(BaseModel):
    name: str
    sessions: list[Session] = Field(default_factory=list)


class EventData(BaseModel):
    sessions: list[Session]
    speakers: list[Speaker]
