"""Package with a Program Retriever that retrieves via HTML."""

from typing import override

from bs4 import BeautifulSoup, Tag

from .exceptions import PageNotFoundException
from .model import EventData, Session
from .page_loader import PageLoader
from .program_retriever import ProgramRetriever


class HtmlProgramRetriever(ProgramRetriever):
    """PRogram retriever for the HTML program."""

    def __init__(self, page_loader: PageLoader) -> None:
        """Set the initial values."""
        self._page_loader = page_loader

    def _get_session_from_session_page(
        self, session_url: str
    ) -> Session | None:
        try:
            session_page = self._page_loader.load_page(session_url)

            soup = BeautifulSoup(session_page, 'html.parser')
            title_tag = soup.find('h1')
            about_tag = soup.select('div.rounded-2xl')
            description_tag = about_tag[0].find('p') if about_tag else None

            title = title_tag.getText().strip() if title_tag else '(Unknown)'
            description = (
                description_tag.getText().strip()
                if description_tag
                else '(Unknown)'
            )
        except PageNotFoundException:
            return None

        return Session(title='', speakers=[])

    def _get_sessions_for_day(self, day_element: Tag) -> list[Session]:
        sessions = day_element.find_all(
            'a',
            href=lambda href: (
                href and href.startswith('/world-congress/agenda/sessions/')
            ),
        )
        unique_urls = {session.get('href', '') for session in sessions}

        session_list: list[Session] = []

        for url in unique_urls:
            sess = self._get_session_from_session_page(
                session_url=f'https://www.wearedevelopers.com{url}'
            )
            if sess:
                session_list.append(sess)

        return session_list

    @override
    def retrieve_program(self) -> EventData:
        contents = self._page_loader.load_page(
            'https://www.wearedevelopers.com/world-congress/agenda/schedule'
        )
        soup = BeautifulSoup(contents, 'html.parser')
        days = soup.select('div[data-grid-panel]')
        for day in days:
            sessions = self._get_sessions_for_day(day)
        return EventData(sessions=[], speakers=[])
