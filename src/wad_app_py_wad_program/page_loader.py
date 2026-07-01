"""Module with PageLoaders.

A PageLoader loads a specific page from a specific URL. This can be by
downloading it from the Internet, or using a local file (for tests).
"""

from abc import ABC, abstractmethod
from typing import override

import requests

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
            'https://www.wearedevelopers.com/world-congress/agenda/schedule': (
                main_filename
            ),
            **session_page_filenames,
        }

    @override
    def load_page(self, url: str) -> str:
        if url not in self._pages:
            raise PageNotFoundException('Page not found')

        with open(self._pages[url]) as infile:
            contents = infile.read()
        return contents


class WebPageLoader(PageLoader):
    """PageLoader for retrieving from the web."""

    def __init__(self) -> None:
        """Set given values for the object."""
        super().__init__()

    @override
    def load_page(self, url: str) -> str:
        response = requests.get(
            url,
            timeout=30,
            headers={
                'User-Agent': (
                    'Mozilla/5.0 (X11; Linux x86_64) '
                    'AppleWebKit/537.36 (KHTML, like Gecko) '
                    'Chrome/126.0.0.0 Safari/537.36'
                )
            },
        )
        if response.status_code == 404:
            raise PageNotFoundException('Page not found')
        response.raise_for_status()
        response.encoding = 'utf-8'
        return response.text
