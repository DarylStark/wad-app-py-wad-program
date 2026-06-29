"""Package with a Program Retriever that retrieves via HTML."""

import re
from collections.abc import Callable
from datetime import date, datetime
from typing import override

from bs4 import BeautifulSoup, Tag

from .exceptions import PageNotFoundException
from .model import EventData, Session, Speaker
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
            id = re.findall('[0-9]+$', session_url)
            id_int = int(id[0]) if id else 0
            soup = BeautifulSoup(session_page, 'html.parser')
            title_tag = soup.find('h1')
            main_topic = ''
            if title_tag:
                main_topic_tag = title_tag.find_previous_sibling()
                main_topic = (
                    main_topic_tag.getText().strip() if main_topic_tag else ''
                )
            about_tag = soup.select('article')
            description_tag = about_tag[0].find('p') if about_tag else None
            topics_tag = soup.select_one('ul.flex')
            topics = []
            if topics_tag:
                topics_tags = topics_tag.find_all('li')
                if topics_tags:
                    topics = [tag.getText().strip() for tag in topics_tag]
                    topics = [topic for topic in topics if topic]

            speakers_tag = soup.select_one('aside')

            title = title_tag.getText().strip() if title_tag else '(Unknown)'
            description = (
                description_tag.getText().strip()
                if description_tag
                else '(Unknown)'
            )

            date_obj: None | date = None
            start_time: datetime | None = None
            end_time: datetime | None = None
            stage = ''

            if title_tag:
                parent_tag = title_tag.find_parent()
                if parent_tag:
                    datetime_and_stage_tag = parent_tag.select_one('div.mt-6')
                    if datetime_and_stage_tag:
                        fields = datetime_and_stage_tag.find_all('span')
                        if len(fields) == 3:
                            date_text = fields[0].getText().strip()
                            time_text = fields[1].getText().strip()
                            current_year = datetime.now().year
                            date_obj = datetime.strptime(
                                f'{date_text} {current_year}',
                                '%A %d %B %Y',
                            ).date()
                            start_time_text, _, end_time_text = (
                                part.strip() for part in time_text.split()
                            )
                            start_time = datetime.strptime(
                                f'{date_obj.isoformat()} {start_time_text}',
                                '%Y-%m-%d %H:%M',
                            )
                            end_time = datetime.strptime(
                                f'{date_obj.isoformat()} {end_time_text}',
                                '%Y-%m-%d %H:%M',
                            )
                            stage = fields[2].getText().split('-')[0].strip()

            # Construct the Session
            page_session = Session(
                id=id_int,
                title=title,
                main_topic=main_topic,
                description=description,
                stage=stage,
                present_date=date_obj,
                start_time=start_time,
                end_time=end_time,
                topics=topics,
                speakers=[],
                url=session_url,
            )

            # Retrieve the speakers
            # TODO: Refactor this mess
            if speakers_tag:
                speakers = speakers_tag.find_all('li')
                if speakers:
                    for speaker_tag in speakers:
                        if not isinstance(speaker_tag, Tag):
                            continue

                        # Get description
                        details_tag = speaker_tag.select_one('details')
                        summary = ''
                        if details_tag:
                            summary_tag = details_tag.select_one('p')
                            summary = (
                                summary_tag.getText().strip()
                                if summary_tag
                                else ''
                            )

                        # Get short information
                        short_tag = speaker_tag.select_one('div.min-w-0')
                        if not short_tag:
                            continue
                        paragraphs = short_tag.find_all('p')
                        if len(paragraphs) != 3:
                            continue
                        name = paragraphs[0].getText().strip()
                        job = (
                            ' '.join(paragraphs[1].getText().split())
                            .strip()
                            .replace('·', '-')
                        )
                        tagline = paragraphs[2].getText().strip()

                        # Construct the Speaker
                        speaker = Speaker(
                            name=name,
                            job=job,
                            tagline=tagline,
                            summary=summary,
                        )
                        page_session.speakers.append(speaker)

            pass
        except PageNotFoundException:
            return None

        return page_session

    def _get_unique_urls_from_schedule_page(
        self, schedule_page_content: str
    ) -> set[str]:
        soup = BeautifulSoup(schedule_page_content, 'html.parser')
        sessions_urls = soup.find_all(
            'a',
            href=lambda href: (
                href and href.startswith('/world-congress/agenda/sessions/')
            ),
        )
        unique_urls = {
            str(session_url.get('href', '')) for session_url in sessions_urls
        }
        return unique_urls

    @override
    def retrieve_program(
        self,
        *,
        hook_total: Callable[[int], None] | None = None,
        hook_progress: Callable[[int], None] | None = None,
    ) -> EventData:
        session_list: list[Session] = []
        contents = self._page_loader.load_page(
            'https://www.wearedevelopers.com/world-congress/agenda/schedule'
        )

        unique_urls = self._get_unique_urls_from_schedule_page(contents)

        if hook_total:
            hook_total(len(unique_urls))

        for done, url in enumerate(unique_urls):
            sess = self._get_session_from_session_page(
                session_url=f'https://www.wearedevelopers.com{url}'
            )
            if sess:
                session_list.append(sess)
            if hook_progress:
                hook_progress(done + 1)

        # TODO: make this a method for `EventData`. Within the `Database` class
        # this is also used and the code is now duplicate.
        speakers: dict[str, Speaker] = {}
        for session in session_list:
            for speaker in session.speakers:
                obj = speakers.setdefault(speaker.name, speaker)
                obj.sessions.append(session)
        return EventData(
            sessions=session_list, speakers=list(speakers.values())
        )
