"""Module with PageLoaders.

A PageLoader loads a specific page from a specific URL. This can be by
downloading it from the Internet, or using a local file (for tests).
"""

from abc import ABC, abstractmethod
from typing import override

from .exceptions import PageNotFoundException


class PageLoader(ABC):
    """Abstract base class for page loaders."""

    @abstractmethod
    def load_page(self, url: str) -> str:
        """Load data for a specific URL."""


class LocalFilePageLoader(PageLoader):
    """PageLoader for local files.

    Primarily used for tests.
    """

    def __init__(
        self, main_filename: str, session_page_filenames: dict[str, str]
    ) -> None:
        """Set given values for the object."""
        super().__init__()
        self._pages: dict[str, str] = {
            'https://www.wearedevelopers.com/world-congress/agenda/schedule': main_filename,
            **session_page_filenames,
        }
        pass

    @override
    def load_page(self, url: str) -> str:
        if url not in self._pages:
            raise PageNotFoundException('Page not found')

        with open(self._pages[url]) as infile:
            contents = infile.read()
        return contents
