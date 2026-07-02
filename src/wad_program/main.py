"""Main entry point for the CLI."""

from enum import Enum
from pathlib import Path

from rich.console import Console
from rich.progress import Progress
from typer import Context, Option, Typer

from .console_visitor import DataType, DetailsVisitor, TableVisitor
from .database_specifications import (
    SpeakerSessionSpecification,
)
from .filters import (
    session_filters,
    session_speaker_filters,
    topic_filters,
)
from .html_program_retriever import HtmlProgramRetriever
from .json_database import JsonDatabase
from .model import (
    Day,
    InterestLevel,
    ModelVisitor,
    Session,
    SessionState,
)
from .page_loader import WebPageLoader
from .wad_program_app import WadProgramApp


class OutputType(Enum):
    """The types of possible output for `list`."""

    TABLE = 'table'
    DETAILS = 'details'


app = Typer(no_args_is_help=True)
console = Console()


@app.command(
    name='sessions',
    help='Manage sessions. This will list all sessions or sessions that '
    'satisfy the given filters. You can optionally perform actions on '
    'the given sessions.',
    short_help='Manager the sessions',
)
def sessions(
    ctx: Context,
    output_type: OutputType = Option(
        default=OutputType.TABLE, help='How to output the data'
    ),
    title_text_i: list[str] = Option(
        default=[], help='Filter: title contains text (case insensitive)'
    ),
    title_text: list[str] = Option(
        default=[],
        help='Filter: title contains text (case sensitive)',
    ),
    description_text_i: list[str] = Option(
        default=[],
        help='Filter: descriptions contains text (case insensitive)',
    ),
    description_text: list[str] = Option(
        default=[],
        help='Filter: description contains text (case sensitive)',
    ),
    any_text_i: list[str] = Option(
        default=[], help='Filter: any text contains text (case insensitive)'
    ),
    any_text: list[str] = Option(
        default=[],
        help='Filter: any text contains text (case sensitive)',
    ),
    main_topic_text_i: list[str] = Option(
        default=[], help='Filter: main topic contains text (case insensitive)'
    ),
    main_topic_text: list[str] = Option(
        default=[],
        help='Filter: main topic contains text (case sensitive)',
    ),
    stage_text_i: list[str] = Option(
        default=[], help='Filter: stage contains text (case insensitive)'
    ),
    stage_text: list[str] = Option(
        default=[],
        help='Filter: stage contains text (case sensitive)',
    ),
    topic_text_i: list[str] = Option(
        default=[],
        help='Filter: one of the topics contains text (case insensitive)',
    ),
    topic_text: list[str] = Option(
        default=[],
        help='Filter: one of the topics contains text (case sensitive)',
    ),
    speaker_any_text_i: list[str] = Option(
        default=[], help='Filter: speaker contains text (case insensitive)'
    ),
    speaker_any_text: list[str] = Option(
        default=[],
        help='Filter: speaker contains contains text (case sensitive)',
    ),
    speaker_tagline_text_i: list[str] = Option(
        default=[],
        help='Filter: speaker tagline contains text (case insensitive)',
    ),
    speaker_tagline_text: list[str] = Option(
        default=[],
        help='Filter: speaker tagline contains contains text (case sensitive)',
    ),
    speaker_name_text_i: list[str] = Option(
        default=[],
        help='Filter: speaker name contains text (case insensitive)',
    ),
    speaker_name_text: list[str] = Option(
        default=[],
        help='Filter: speaker job contains contains text (case sensitive)',
    ),
    speaker_job_text_i: list[str] = Option(
        default=[],
        help='Filter: speaker job contains text (case insensitive)',
    ),
    speaker_job_text: list[str] = Option(
        default=[],
        help='Filter: speaker name contains contains text (case sensitive)',
    ),
    filter_id: int | None = Option(
        default=None,
        help='Filter: specific ID',
    ),
    state: SessionState | None = Option(
        default=None,
        help='Filter: specific state',
    ),
    start_time_after: str | None = Option(
        default=None,
        help='Filter: session starts at or after a specific time '
        '(format: HH:MM)',
    ),
    end_time_before: str | None = Option(
        default=None,
        help='Filter: session end at or before a specific time '
        '(format: HH:MM)',
    ),
    day: Day | None = Option(
        default=None, help='Filter: sessions at a specific day'
    ),
    interest_level: InterestLevel | None = Option(
        default=None, help='Filter: specific interest level.'
    ),
    set_state: SessionState | None = Option(
        default=None, help='Action: Set session state'
    ),
    set_interest_level: InterestLevel | None = Option(
        default=None, help='Action: Set interest level'
    ),
) -> None:
    """List sessions currently in the database."""
    console = ctx.obj['console']
    wad = ctx.obj['wad']

    spec = session_filters.build(ctx.params)
    speaker_filter = [
        filter
        for filter_name, filter in ctx.params.items()
        if filter_name.startswith('speaker_') and filter
    ]
    if speaker_filter:
        spec.add_specification(
            SpeakerSessionSpecification(
                session_speaker_filters.build(ctx.params)
            )
        )

    # Retrieve sessions
    sessions: list[Session] = wad.get_sessions(spec)

    # Actions
    if set_state or set_interest_level:
        for session in sessions:
            if set_state:
                session.state = set_state
            if set_interest_level:
                session.interest_level = set_interest_level

        # Save the database
        wad.save_database()

    # Generate output
    output_visitors = {
        OutputType.TABLE: TableVisitor(console, DataType.SESSIONS),
        OutputType.DETAILS: DetailsVisitor(console),
    }

    visitor: ModelVisitor = output_visitors[output_type]
    for session in sessions:
        session.accept(visitor)
    visitor.done()


@app.command(
    name='topics',
    help='Show topics.',
    short_help='Show topics.',
)
def topics(
    ctx: Context,
    output_type: OutputType = Option(
        default=OutputType.TABLE, help='How to output the data'
    ),
    name_text_i: list[str] = Option(
        default=[], help='Filter: name contains text (case insensitive)'
    ),
    name_text: list[str] = Option(
        default=[],
        help='Filter: name contains text (case sensitive)',
    ),
    main_topic: bool | None = Option(
        default=None,
        help='Filter: show only main topics',
    ),
) -> None:
    """Show topics in the database."""
    console = ctx.obj['console']
    wad = ctx.obj['wad']

    # Get the topics
    topics = wad.get_topics(topic_filters.build(ctx.params))

    # Generate output
    output_visitors = {
        OutputType.TABLE: TableVisitor(console, DataType.TOPICS),
        OutputType.DETAILS: DetailsVisitor(console),
    }

    visitor: ModelVisitor = output_visitors[output_type]
    for topic in topics:
        topic.accept(visitor)
    visitor.done()


@app.command(
    name='update', help='Update the sessions', short_help='Update the sessions'
)
def update(
    ctx: Context,
) -> None:
    """Update the sessions in the database."""
    console = ctx.obj['console']
    with Progress(console=console) as progress:
        retrieve_sessions = progress.add_task('Retrieving', total=0)
        syncing_database = progress.add_task('Syncing database', total=0)
        updating_speaker_list = progress.add_task('Updating speakers', total=0)

        ctx.obj['wad'].update_database(
            hook_retrieve_total=lambda total: progress.update(
                retrieve_sessions, total=total
            ),
            hook_retrieve_progress=lambda completed: progress.update(
                retrieve_sessions, completed=completed
            ),
            hook_sync_total=lambda total: progress.update(
                syncing_database, total=total
            ),
            hook_sync_progress=lambda completed: progress.update(
                syncing_database, completed=completed
            ),
            hook_speaker_list_total=lambda total: progress.update(
                updating_speaker_list, total=total
            ),
            hook_speaker_list_progress=lambda completed: progress.update(
                updating_speaker_list, completed=completed
            ),
        )


@app.callback()
def common_command_line_options(
    ctx: Context,
    json_filename: Path = Option(
        default='~/wadprogram.json',
        envvar='WADPROGRAM_DB_FILE',
        writable=True,
        readable=True,
        resolve_path=False,
    ),
) -> None:
    """Default callback for the command line options.

    Will always be called before the correct command is called. This way, we
    can setup a object that is used by all commands.
    """
    ctx.obj = {
        'console': console,
        'wad': WadProgramApp(
            retriever=HtmlProgramRetriever(WebPageLoader()),
            database=JsonDatabase(
                json_filename=str(json_filename.expanduser().resolve())
            ),
        ),
    }


def main() -> None:
    """Main entry point for the application.

    Will start the Typer app for the CLI arguments.
    """
    app()
