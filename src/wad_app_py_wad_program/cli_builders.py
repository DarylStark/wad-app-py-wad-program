"""Module with CLI builders.

CLI builders are help tools for the CLI. They build, for instance,
specifications when giving a specific set of filters.
"""

from collections.abc import Callable
from typing import Any, TypeVar

from .database_specifications import (
    CompositeSpecification,
    FieldComparisonOperatorSpecification,
    TextContainsSpecification,
)

T = TypeVar('T')
type TextContainsSpecBuildDict[T] = dict[
    str, Callable[[str], TextContainsSpecification[T]]
]

type EqualitySpecBuildDict[T] = dict[
    str, Callable[[str], FieldComparisonOperatorSpecification[T]]
]


def build_text_specification[T](
    spec_build_dict: TextContainsSpecBuildDict[T],
    params: dict[str, tuple[Any]],
) -> CompositeSpecification[T]:
    """Function to build a Composite Specification for text filters."""
    specs = CompositeSpecification[T]()
    for filter, builder in spec_build_dict.items():
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


def build_equality_specification[T](
    spec_build_dict: EqualitySpecBuildDict[T], params: dict[str, Any]
) -> CompositeSpecification[T]:
    """Function to build a Composite Specification for equality filters."""
    specs = CompositeSpecification[T]()
    for filter, builder in spec_build_dict.items():
        if filter in params and params.get(filter) is not None:
            specs.add_specification(builder(params[filter]))
            pass
    return specs
