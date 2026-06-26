"""Module with a ModelVisitor for Console output."""

from typing import override

from rich.console import Console
from rich.table import Table

from .model import ModelVisitor, Session


class TableVisitor(ModelVisitor):
    """Output sessions to a table."""

    def __init__(self, console: Console) -> None:
        """Create the table."""
        self._console = console
        self._table = Table()
        self._table.add_column('#')
        self._table.add_column('State')
        self._table.add_column('Date')
        self._table.add_column('Starttime')
        self._table.add_column('Endtime')
        self._table.add_column('Title')

    @override
    def visit_session(self, session: Session) -> None:
        """Add a session to the table."""
        self._table.add_row(
            str(session.id),
            session.state.value.capitalize(),
            str(session.start_time),
            str(session.start_time),
            str(session.end_time),
            session.title,
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
