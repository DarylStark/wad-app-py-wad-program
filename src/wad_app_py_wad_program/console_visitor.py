"""Module with a ModelVisitor for Console output."""

from typing import override

from rich import box
from rich.console import Console, Group
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.columns import Columns

from .model import ModelVisitor, Session


class TableVisitor(ModelVisitor):
    """Output sessions to a table."""

    def __init__(self, console: Console) -> None:
        """Create the table."""
        self._console = console
        self._table = Table(box=box.SIMPLE)
        self._table.add_column('#')
        self._table.add_column('State')
        self._table.add_column('Day')
        self._table.add_column('Stage')
        self._table.add_column('Start')
        self._table.add_column('End')
        self._table.add_column('Min')
        self._table.add_column('Title')
        self._table.add_column('Main topic')
        self._table.add_column('Topics')
        self._table.add_column('Speakers')

    @override
    def visit_session(self, session: Session) -> None:
        """Add a session to the table."""
        self._table.add_row(
            str(session.id),
            session.state.value.capitalize(),
            session.stage,
            session.start_time.strftime('%a'),
            session.start_time.strftime('%H:%M'),
            session.end_time.strftime('%H:%M'),
            f'{session.duration.seconds / 60:.0f}',
            session.title,
            session.main_topic,
            ', '.join(session.topics),
            ', '.join([speaker.name for speaker in session.speakers])
        )

    @override
    def done(self) -> None:
        """Print the table."""
        self._console.print(self._table)


class DetailsVisitor(ModelVisitor):
    """Output sessions with details."""

    def __init__(self, console: Console) -> None:
        """Create the table."""
        self._console = console

    @override
    def visit_session(self, session: Session) -> None:
        """Add a session to the table."""
        header = f'[b][yellow]{session.title}[/yellow][/b] ([green]{session.main_topic}[/]) - {session.state.value.capitalize()}\n'
        header += f'[bright_black][b]{session.start_time.strftime("%A")}[/b], from [b]{session.start_time.strftime("%H:%M")}[/b] till [b]{session.end_time.strftime("%H:%M")}[/b] at [b]{session.stage}[/b][/] ({session.duration.seconds / 60:.0f} minutes)\n'

        text = session.description

        footer = f'[b][green]Topics:[/green][/b] {', '.join(session.topics)}'

        speakers: list[str] = []
        for speaker in session.speakers:
            speakers.append(f'[b][orange]{speaker.name}[/orange][/b] ([bright_black]{speaker.job}[/bright_black])\n[i][bright_black]{speaker.tagline}[/bright_black][/i]\n\n{speaker.summary}')

        panel = Panel(Group(header, text, '\n', footer, '\n', '\n\n\n'.join(speakers)))
        self._console.print(panel)

    @override
    def done(self) -> None:
        """Does nothing."""
