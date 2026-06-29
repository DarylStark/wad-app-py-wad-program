"""Module with a ModelVisitor for Console output."""

from typing import override

from rich import box
from rich.console import Console
from rich.table import Table

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
        self._console.print(f'Session: {session.title}')

    @override
    def done(self) -> None:
        """Does nothing."""
