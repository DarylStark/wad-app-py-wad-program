"""Module with a ModelVisitor for Console output."""

from datetime import datetime
from enum import Enum
from typing import override

from rich import box
from rich.console import Console, Group
from rich.panel import Panel
from rich.table import Table

from .model import InterestLevel, ModelVisitor, Session, SessionState, Topic


class DataType(Enum):
    """Type of data for Visitors."""

    SESSIONS = 'sessions'
    TOPICS = 'topics'


class ConsoleVisitor(ModelVisitor):
    """Base class for console visitors."""

    def _convert_datetime_to_format(
        self, dt: datetime | None, format: str
    ) -> str:
        if not dt:
            return 'Unknown'
        return dt.strftime(format)


class TableVisitor(ConsoleVisitor):
    """Output sessions to a table."""

    def __init__(self, console: Console, data_type: DataType) -> None:
        """Create the table."""
        self._item_count = 0

        self._console = console

        self._table = Table(box=box.SIMPLE)

        if data_type == DataType.SESSIONS:
            self._table.add_column('#')
            self._table.add_column('State')
            self._table.add_column('Interest')
            self._table.add_column('Day')
            self._table.add_column('Stage')
            self._table.add_column('Start')
            self._table.add_column('End')
            self._table.add_column('Min')
            self._table.add_column('Title')
            self._table.add_column('Main topic')
            self._table.add_column('Topics')
            self._table.add_column('Speakers')
        elif data_type == DataType.TOPICS:
            self._table.add_column('Name')
            self._table.add_column('Is main topic')

    def _get_state_str(self, state: SessionState) -> str:
        color = 'yellow'
        if state == SessionState.ACTIVE:
            color = 'green'
        elif state == SessionState.REMOVED:
            color = 'bright_black'
        return f'[{color}]{state.value.capitalize()}[/{color}]'

    def _get_interest_level_str(self, interest_level: InterestLevel) -> str:
        color = 'red'
        if interest_level == InterestLevel.NOT_INTERESTED:
            color = 'bright_black'
        elif interest_level == InterestLevel.WATCH_LATER:
            color = 'blue'
        elif interest_level == InterestLevel.ALTERNATIVE:
            color = 'yellow'
        elif interest_level == InterestLevel.INTERESTED:
            color = 'green'
        return (
            f'[{color}]'
            '{interest_level.value.replace("_", " ").capitalize()}[/{color}]'
        )

    @override
    def visit_session(self, session: Session) -> None:
        """Add a session to the table."""
        self._table.add_row(
            str(session.id),
            self._get_state_str(session.state),
            self._get_interest_level_str(session.interest_level),
            session.stage,
            self._convert_datetime_to_format(session.start_time, '%a'),
            self._convert_datetime_to_format(session.start_time, '%H:%M'),
            self._convert_datetime_to_format(session.end_time, '%H:%M'),
            f'{session.duration.seconds / 60:.0f}',
            session.title,
            session.main_topic,
            ', '.join(session.topics),
            ', '.join([speaker.name for speaker in session.speakers]),
        )
        self._item_count += 1

    @override
    def visit_topic(self, topic: Topic) -> None:
        """Add a topic to the table."""
        self._table.add_row(topic.name, 'Yes' if topic.is_main_topic else 'No')
        self._item_count += 1

    @override
    def done(self) -> None:
        """Print the table."""
        if self._item_count:
            self._console.print(
                f'\n  [green]Found [b]{self._item_count}[/b] sessions '
                'that match your current filter[/green]'
            )
            self._console.print(self._table)
        else:
            self._console.print(
                '[yellow]There were no sessions for your '
                'given filter.[/yellow]'
            )


class DetailsVisitor(ConsoleVisitor):
    """Output sessions with details."""

    def __init__(self, console: Console) -> None:
        """Create the table."""
        self._console = console

    @override
    def visit_session(self, session: Session) -> None:
        """Add a session to the table."""
        header = (
            f'[b][yellow]{session.title}[/yellow][/b] '
            f'([green]{session.main_topic}[/]) - '
            f'{session.state.value.capitalize()}\n'
        )
        day = self._convert_datetime_to_format(session.start_time, '%A')
        starttime = self._convert_datetime_to_format(
            session.start_time, '%H:%M'
        )
        endtime = self._convert_datetime_to_format(session.end_time, '%H:%M')
        header += (
            f'[bright_black][b]{day}[/b], '
            f'from [b]{starttime}[/b] till [b]'
            f'{endtime}[/b] at '
            f'[b]{session.stage}[/b][/] '
            f'({session.duration.seconds / 60:.0f} minutes)\n'
        )

        text = session.description

        footer = f'[b][green]Topics:[/green][/b] {", ".join(session.topics)}'

        speakers: list[str] = []
        for speaker in session.speakers:
            speakers.append(
                f'[b][orange]{speaker.name}[/orange][/b] '
                f'([bright_black]{speaker.job}[/bright_black])\n[i]'
                f'[bright_black]{speaker.tagline}[/bright_black][/i]'
                f'\n\n{speaker.summary}'
            )

        panel = Panel(
            Group(header, text, '\n', footer, '\n', '\n\n\n'.join(speakers))
        )
        self._console.print(panel)

    @override
    def visit_topic(self, topic: Topic) -> None:
        """Add a topic to the table."""
        pass

    @override
    def done(self) -> None:
        """Does nothing."""
