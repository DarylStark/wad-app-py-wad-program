"""Module with Specifications for the database."""

from abc import ABC, abstractmethod
from typing import override

from .model import Session, Speaker, SessionState


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
SpeakerSpecification = Specification[Speaker]
SessionCompositeSpecification = CompositeSpecification[Session]
SpeakerCompositeSpecification = CompositeSpecification[Speaker]


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
        fields_to_search = ['title', 'main_topic', 'description']
        found = []
        for field in fields_to_search:
            value = getattr(obj, field)
            if self._case_sensitive:
                self._text.lower()
                value.lower()
            found.append(self._text in value)
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
