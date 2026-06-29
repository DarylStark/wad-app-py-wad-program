"""Module with Specifications for the database."""

from abc import ABC, abstractmethod
from datetime import time
from typing import override

from .model import Day, Session, SessionState, Speaker, Topic


class Specification[T](ABC):
    """Abstract, generic base class for specifications."""

    @abstractmethod
    def is_satisfied_by(self, obj: T) -> bool:
        """Determines if the specification is valid."""


class CompositeSpecification[T](Specification[T]):
    """Composite specification."""

    def __init__(self) -> None:
        """Create empty list of specifications."""
        self._specs: list[Specification[T]] = []

    def add_specification(self, spec: Specification[T]) -> None:
        """Add a specification to the composite."""
        self._specs.append(spec)

    @override
    def is_satisfied_by(self, obj: T) -> bool:
        """Check if all specifications are True."""
        if not self._specs:
            return True
        return all(spec.is_satisfied_by(obj) for spec in self._specs)


SessionSpecification = Specification[Session]
SessionCompositeSpecification = CompositeSpecification[Session]
SpeakerSpecification = Specification[Speaker]
SpeakerCompositeSpecification = CompositeSpecification[Speaker]
TopicSpecification = Specification[Topic]
TopicCompositeSpecification = CompositeSpecification[Topic]


class TitleContainsSpecification(SessionSpecification):
    """Specification for sessions with a specific text in the title."""

    def __init__(self, text: str, case_sensitive: bool = True) -> None:
        """Set the text to search for."""
        self._text = text
        self._case_sensitive = case_sensitive

    def _is_satisfied_by_case_sensitive(self, obj: Session) -> bool:
        return self._text in obj.title

    def _is_satisfied_by_case_insensitive(self, obj: Session) -> bool:
        return self._text.lower() in obj.title.lower()

    @override
    def is_satisfied_by(self, obj: Session) -> bool:
        if self._case_sensitive:
            return self._is_satisfied_by_case_sensitive(obj)
        return self._is_satisfied_by_case_insensitive(obj)


class DescriptionContainsSpecification(SessionSpecification):
    """Specification for sessions with a specific text in the description."""

    def __init__(self, text: str, case_sensitive: bool = True) -> None:
        """Set the text to search for."""
        self._text = text
        self._case_sensitive = case_sensitive

    def _is_satisfied_by_case_sensitive(self, obj: Session) -> bool:
        return self._text in obj.description

    def _is_satisfied_by_case_insensitive(self, obj: Session) -> bool:
        return self._text.lower() in obj.description.lower()

    @override
    def is_satisfied_by(self, obj: Session) -> bool:
        if self._case_sensitive:
            return self._is_satisfied_by_case_sensitive(obj)
        return self._is_satisfied_by_case_insensitive(obj)


class AnyTextContainsSpecification(SessionSpecification):
    """Specification for sessions with a specific text in one of the fields."""

    def __init__(self, text: str, case_sensitive: bool = True) -> None:
        """Set the text to search for."""
        self._text = text
        self._case_sensitive = case_sensitive

    @override
    def is_satisfied_by(self, obj: Session) -> bool:
        found: list[bool] = []

        # Search in "normal" text fields
        fields_to_search = ['title', 'main_topic', 'description', 'main_topic']
        for field in fields_to_search:
            value = getattr(obj, field)
            if not self._case_sensitive:
                self._text = self._text.lower()
                value = value.lower()
            found.append(self._text in value)

        # Serach in Topics
        value = ' '.join(obj.topics)
        if not self._case_sensitive:
            self.text = self._text.lower()
            value = value.lower()
        found.append(self._text in value)

        # Only return if any of them are True
        return any(found)


class IdSpecification(SessionSpecification):
    """Specification for sessions with a specific ID."""

    def __init__(self, search_id: int) -> None:
        """Set the id to search for."""
        self._id = search_id

    @override
    def is_satisfied_by(self, obj: Session) -> bool:
        return obj.id == self._id


class StateSpecification(SessionSpecification):
    """Specification for sessions with a specific state."""

    def __init__(self, state: SessionState) -> None:
        """Set the id to search for."""
        self._state = state

    @override
    def is_satisfied_by(self, obj: Session) -> bool:
        return obj.state == self._state


class MainTopicSpecification(SessionSpecification):
    """Specification for sessions with a specific text in the main topic."""

    def __init__(self, text: str, case_sensitive: bool = True) -> None:
        """Set the text to search for."""
        self._text = text
        self._case_sensitive = case_sensitive

    def _is_satisfied_by_case_sensitive(self, obj: Session) -> bool:
        return self._text in obj.main_topic

    def _is_satisfied_by_case_insensitive(self, obj: Session) -> bool:
        return self._text.lower() in obj.main_topic.lower()

    @override
    def is_satisfied_by(self, obj: Session) -> bool:
        if self._case_sensitive:
            return self._is_satisfied_by_case_sensitive(obj)
        return self._is_satisfied_by_case_insensitive(obj)


class StageSpecification(SessionSpecification):
    """Specification for sessions with a specific text in the stage."""

    def __init__(self, text: str, case_sensitive: bool = True) -> None:
        """Set the text to search for."""
        self._text = text
        self._case_sensitive = case_sensitive

    def _is_satisfied_by_case_sensitive(self, obj: Session) -> bool:
        return self._text in obj.stage

    def _is_satisfied_by_case_insensitive(self, obj: Session) -> bool:
        return self._text.lower() in obj.stage.lower()

    @override
    def is_satisfied_by(self, obj: Session) -> bool:
        if self._case_sensitive:
            return self._is_satisfied_by_case_sensitive(obj)
        return self._is_satisfied_by_case_insensitive(obj)


class StartTimeAtOrAfterSpecification(SessionSpecification):
    """Specification for sessions with a starttime at or after."""

    def __init__(self, start_time: time) -> None:
        """Set the starttime to search for."""
        self._start_time = start_time

    @override
    def is_satisfied_by(self, obj: Session) -> bool:
        return self._start_time <= obj.start_time.time()


class EndTimeAtOrBeforeSpecification(SessionSpecification):
    """Specification for sessions with a endtime at or before."""

    def __init__(self, end_time: time) -> None:
        """Set the end time to search for."""
        self._end_time = end_time

    @override
    def is_satisfied_by(self, obj: Session) -> bool:
        return obj.end_time.time() <= self._end_time


class SpecificDaySpecification(SessionSpecification):
    """Specification for sessions at a specific day."""

    def __init__(self, day: Day) -> None:
        """Set the day to filter on."""
        self._day = day

    @override
    def is_satisfied_by(self, obj: Session) -> bool:
        return obj.start_time.isoweekday() == self._day.iso_day_number


class InterestLevelSpecification(SessionSpecification):
    """Specification for sessions with a specific Interest level."""

    def __init__(self, level: InterestLevel) -> None:
        """Set the level to filter on."""
        self._level = level

    @override
    def is_satisfied_by(self, obj: Session) -> bool:
        return obj.interest_level == self._level


class SpeakerSessionSpecification(SessionSpecification):
    """Specification for a session to filter on speaker.

    This specification takes a SpeakerSpecification in it's constructor and
    will only validate to True when one of the speakers satisfied the
    specification.
    """

    def __init__(self, speaker_spec: SpeakerSpecification) -> None:
        """Set the speaker specification to search for."""
        self._speaker_spec = speaker_spec

    @override
    def is_satisfied_by(self, obj: Session) -> bool:
        found: list[bool] = [
            self._speaker_spec.is_satisfied_by(speaker)
            for speaker in obj.speakers
        ]
        return any(found)


class SpeakerAnyTextSpecification(SpeakerSpecification):
    """Specification that is satisfied by any text."""

    def __init__(self, text: str, case_sensitive: bool = True) -> None:
        """Set the text to search for."""
        self._text = text
        self._case_sensitive = case_sensitive

    @override
    def is_satisfied_by(self, obj: Speaker) -> None:
        found: list[bool] = []

        # Search in "normal" text fields
        fields_to_search = ['name', 'job', 'tagline', 'summary']
        for field in fields_to_search:
            value = getattr(obj, field)
            if not self._case_sensitive:
                self._text = self._text.lower()
                value = value.lower()
            found.append(self._text in value)

        return any(found)


class TaglineContainsSpecification(SpeakerSpecification):
    """Specification for speakers with a specific text in the tagline."""

    def __init__(self, text: str, case_sensitive: bool = True) -> None:
        """Set the text to search for."""
        self._text = text
        self._case_sensitive = case_sensitive

    def _is_satisfied_by_case_sensitive(self, obj: Speaker) -> bool:
        return self._text in obj.tagline

    def _is_satisfied_by_case_insensitive(self, obj: Speaker) -> bool:
        return self._text.lower() in obj.tagline.lower()

    @override
    def is_satisfied_by(self, obj: Speaker) -> bool:
        if self._case_sensitive:
            return self._is_satisfied_by_case_sensitive(obj)
        return self._is_satisfied_by_case_insensitive(obj)


class NameContainsSpecification(SpeakerSpecification):
    """Specification for speakers with a specific text in the name."""

    def __init__(self, text: str, case_sensitive: bool = True) -> None:
        """Set the text to search for."""
        self._text = text
        self._case_sensitive = case_sensitive

    def _is_satisfied_by_case_sensitive(self, obj: Speaker) -> bool:
        return self._text in obj.name

    def _is_satisfied_by_case_insensitive(self, obj: Speaker) -> bool:
        return self._text.lower() in obj.name.lower()

    @override
    def is_satisfied_by(self, obj: Speaker) -> bool:
        if self._case_sensitive:
            return self._is_satisfied_by_case_sensitive(obj)
        return self._is_satisfied_by_case_insensitive(obj)

class TopicNameContainsSpecification(TopicSpecification):
    """Specification for topics that contains text in the name."""

    def __init__(self, text: str, case_sensitive: bool = True) -> None:
        """Set the text to search for."""
        self._text = text
        self._case_sensitive = case_sensitive

    def _is_satisfied_by_case_sensitive(self, obj: Topic) -> bool:
        return self._text in obj.name

    def _is_satisfied_by_case_insensitive(self, obj: Topic) -> bool:
        return self._text.lower() in obj.name.lower()

    @override
    def is_satisfied_by(self, obj: Topic) -> bool:
        if self._case_sensitive:
            return self._is_satisfied_by_case_sensitive(obj)
        return self._is_satisfied_by_case_insensitive(obj)
