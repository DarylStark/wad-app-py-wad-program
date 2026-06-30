"""Module with specification builders."""

from collections.abc import Callable
from typing import Any

from pydantic import BaseModel

from .database_specifications import (
    CompositeSpecification,
    FieldComparisonOperatorSpecification,
    TextContainsSpecification,
)

type TextContainsSpecBuildDict[T] = dict[
    str, Callable[[str], TextContainsSpecification[T]]
]

type ComparisonSpecBuildDict[T] = dict[
    str, Callable[[str], FieldComparisonOperatorSpecification[T]]
]


class FilterSpecifications[T](BaseModel):
    """DTO for filters."""

    text: TextContainsSpecBuildDict[T] | None = None
    comparison: ComparisonSpecBuildDict[T] | None = None

    def _build_text_specification(
        self,
        params: dict[str, tuple[Any]],
    ) -> CompositeSpecification[T]:
        """Method to build a Composite Specification for text filters."""
        specs = CompositeSpecification[T]()
        if not self.text:
            return specs

        for filter, builder in self.text.items():
            filter_arg_sensitive = f'{filter}_text'
            filter_arg_insensitive = f'{filter}_text_i'

            if (
                filter_arg_sensitive in params
                and type(params[filter_arg_sensitive]) is tuple
            ):
                for text in params[filter_arg_sensitive]:
                    spec = builder(text)
                    spec.set_case_sensitivity(True)
                    specs.add_specification(spec)

            if (
                filter_arg_insensitive in params
                and type(params[filter_arg_insensitive]) is tuple
            ):
                for text in params[filter_arg_insensitive]:
                    spec = builder(text)
                    spec.set_case_sensitivity(False)
                    specs.add_specification(spec)
        return specs

    def _build_comparison_specification(
        self, params: dict[str, Any]
    ) -> CompositeSpecification[T]:
        """Method to build a Composite Specification for equality filters."""
        specs = CompositeSpecification[T]()
        if not self.comparison:
            return specs

        for filter, builder in self.comparison.items():
            if filter in params and params.get(filter) is not None:
                specs.add_specification(builder(params[filter]))

        return specs

    def build(self, params: dict[str, Any]) -> CompositeSpecification[T]:
        """Create the Specification objects for a specific filter spec."""
        specs = CompositeSpecification[T]()
        specs.add_specification(self._build_text_specification(params))
        specs.add_specification(self._build_comparison_specification(params))
        return specs
