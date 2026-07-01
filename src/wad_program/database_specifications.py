"""Module with Specifications for the database."""

from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, override

from .model import Session, Speaker, Topic


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


class TextContainsSpecification[T](Specification[T]):
    """Specification to check if text is included."""

    def __init__(self, text: str, fields: list[str]) -> None:
        """Set default values."""
        self._text = text
        self._fields = fields
        self._case_sensitivity = True

    def set_case_sensitivity(self, sensitiviy: bool) -> None:
        """Set the case sensitivity for the text filter."""
        self._case_sensitivity = sensitiviy

    def _is_satisfied_for_field(self, field_value: str) -> bool:
        if not self._case_sensitivity:
            self._text = self._text.lower()
            field_value = field_value.lower()
        return self._text in field_value

    @override
    def is_satisfied_by(self, obj: T) -> bool:
        satifisfactions: list[bool] = []
        for field in self._fields:
            value = getattr(obj, field)
            if type(value) is list:
                value = ', '.join(value)
            if type(value) is not str:
                continue
            satifisfactions.append(self._is_satisfied_for_field(value))
        return any(satifisfactions)


class ComparisonOperator(Enum):
    """Enum to specify which comparison operator to use."""

    EQUALS = 0
    LE = 1
    LT = 2
    GE = 3
    GT = 4
    NOT_EQUALS = 5


class FieldComparisonOperatorSpecification[T](Specification[T]):
    """Specification to check a binary operator for a specific field."""

    def __init__(
        self,
        value: Any,  # noqa: ANN401
        field: str,
        operator: ComparisonOperator,
    ) -> None:
        """Set default values."""
        self._value = value
        self._field = field
        self._operator = operator

    def _is_satisfied_by_equals(self, obj: T) -> bool:
        return self._value == getattr(obj, self._field)

    def _is_satisfied_by_le(self, obj: T) -> bool:
        return self._value <= getattr(obj, self._field)

    def _is_satisfied_by_lt(self, obj: T) -> bool:
        return self._value < getattr(obj, self._field)

    def _is_satisfied_by_ge(self, obj: T) -> bool:
        return self._value >= getattr(obj, self._field)

    def _is_satisfied_by_gt(self, obj: T) -> bool:
        return self._value > getattr(obj, self._field)

    def _is_satisfied_by_not(self, obj: T) -> bool:
        return self._value != getattr(obj, self._field)

    @override
    def is_satisfied_by(self, obj: T) -> bool:
        operator_methods = {
            ComparisonOperator.EQUALS: self._is_satisfied_by_equals,
            ComparisonOperator.LE: self._is_satisfied_by_le,
            ComparisonOperator.LT: self._is_satisfied_by_lt,
            ComparisonOperator.GE: self._is_satisfied_by_ge,
            ComparisonOperator.GT: self._is_satisfied_by_gt,
            ComparisonOperator.NOT_EQUALS: self._is_satisfied_by_not,
        }
        return operator_methods[self._operator](obj)


SessionSpecification = Specification[Session]
SessionCompositeSpecification = CompositeSpecification[Session]
SessionTextContainsSpecification = TextContainsSpecification[Session]
SpeakerSpecification = Specification[Speaker]
SpeakerCompositeSpecification = CompositeSpecification[Speaker]
SpeakerTextContainsSpecification = TextContainsSpecification[Speaker]
TopicSpecification = Specification[Topic]
TopicCompositeSpecification = CompositeSpecification[Topic]
TopicTextContainsSpecification = TextContainsSpecification[Topic]


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
