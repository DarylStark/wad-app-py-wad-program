from abc import ABC, abstractmethod
from typing import override

from .exceptions import PageNotFoundException


class PageLoader(ABC):
    def __init__(self) -> None:
        self._contents: str | None = None

    @abstractmethod
    def load_page(self, url: str) -> str:
        """Load data for a specific page."""


class LocalFilePageLoader(PageLoader):
    def __init__(
        self, main_filename: str, session_page_filenames: dict[str, str]
    ) -> None:
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
