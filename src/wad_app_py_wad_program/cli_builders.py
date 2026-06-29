"""Module with CLI builders.

CLI builders are help tools for the CLI. They build, for instance,
specifications when giving a specific set of filters.
"""

from collections.abc import Callable
from typing import Any, TypeVar

from .database_specifications import (
    CompositeSpecification,
    TextContainsSpecification,
)

T = TypeVar('T')
type SpecBuildDict[T] = dict[
    str, Callable[[str], TextContainsSpecification[T]]
]


def build_text_specification[T](
    spec_build_dict: SpecBuildDict[T], params: dict[str, tuple[Any]]
) -> CompositeSpecification[T]:
    """Function to build a Composite Specification for specific filters."""
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
