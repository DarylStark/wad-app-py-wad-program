"""Main entry point for the CLI."""

from enum import Enum

from rich.console import Console
from rich.progress import Progress
from typer import Context, Option, Typer

from .console_visitor import DetailsVisitor, TableVisitor
from .database_specifications import (
    AnyTextContainsSpecification,
    DescriptionContainsSpecification,
    IdSpecification,
    MainTopicSpecification,
    SessionCompositeSpecification,
    StateSpecification,
    TitleContainsSpecification,
    SpeakerAnyTextSpecification,
    SpeakerSessionSpecification,
    TaglineContainsSpecification,
    NameContainsSpecification,
)
from .html_program_retriever import HtmlProgramRetriever
from .json_database import JsonDatabase
from .model import ModelVisitor, Session, SessionState
from .page_loader import WebPageLoader
from .wad_program_app import WadProgramApp


class OutputType(Enum):
    """The types of possible output for `list`."""

    TABLE = 'table'
    DETAILS = 'details'


app = Typer(no_args_is_help=True)
console = Console()


@app.command(
    name='list-sessions',
    help='List the sessions',
    short_help='List the sessions',
)
def list_sessions(
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
    text_i: list[str] = Option(
        default=[], help='Filter: text contains text (case insensitive)'
    ),
    text: list[str] = Option(
        default=[],
        help='Filter: text contains text (case sensitive)',
    ),
    filter_id: int | None = Option(
        default=None,
        help='Filter: specific ID',
    ),
    state: SessionState | None = Option(
        default=None,
        help='Filter: specific state',
    ),
    main_topic_text_i: list[str] = Option(
        default=[], help='Filter: main topic contains text (case insensitive)'
    ),
    main_topic_text: list[str] = Option(
        default=[],
        help='Filter: main topic contains text (case sensitive)',
    ),
    speaker_text_i: list[str] = Option(
        default=[],
        help='Filter: speaker contains text (case insensitive)'
    ),
    speaker_text: list[str] = Option(
        default=[],
        help='Filter: speaker contains contains text (case sensitive)',
    ),
    speaker_tagline_text_i: list[str] = Option(
        default=[],
        help='Filter: speaker tagline contains text (case insensitive)'
    ),
    speaker_tagline_text: list[str] = Option(
        default=[],
        help='Filter: speaker tagline contains contains text (case sensitive)',
    ),
    speaker_name_text_i: list[str] = Option(
        default=[],
        help='Filter: speaker name contains text (case insensitive)'
    ),
    speaker_name_text: list[str] = Option(
        default=[],
        help='Filter: speaker name contains contains text (case sensitive)',
    ),
) -> None:
    """List sessions currently in the database."""
    console = ctx.obj['console']
    wad = ctx.obj['wad']

    spec = SessionCompositeSpecification()

    # Configure all filters with their specifications
    filters = {
        'title_i': (title_text_i, TitleContainsSpecification, False),
        'title': (title_text, TitleContainsSpecification, True),
        'desc_i': (
            description_text_i,
            DescriptionContainsSpecification,
            False,
        ),
        'desc': (description_text, DescriptionContainsSpecification, True),
        'text': (text, AnyTextContainsSpecification, True),
        'text_i': (text_i, AnyTextContainsSpecification, False),
        'main_topic_text_i': (
            main_topic_text_i,
            MainTopicSpecification,
            False,
        ),
        'main_topic_text': (main_topic_text, MainTopicSpecification, True),
    }

    # Apply all text filters
    for texts, spec_class, case_sensitive in filters.values():
        for input_text in texts:
            spec.add_specification(spec_class(input_text, case_sensitive))

    # Filter for Speakers
    speaker_filters = {
        'speaker_text': (speaker_text, SpeakerAnyTextSpecification, True),
        'speaker_text_i': (speaker_text_i, SpeakerAnyTextSpecification, False),
        'speaker_tagline_text': (speaker_tagline_text, TaglineContainsSpecification, True),
        'speaker_tagline_text_i': (speaker_tagline_text_i, TaglineContainsSpecification, False),
        'speaker_name_text': (speaker_name_text, NameContainsSpecification, True),
        'speaker_name_text_i': (speaker_name_text_i, NameContainsSpecification, False),
    }

    # Apply text filters for speakers
    for texts, spec_class, case_sensitive in speaker_filters.values():
        for input_text in texts:
            spec.add_specification(
                SpeakerSessionSpecification(
                    spec_class(input_text, case_sensitive)
                )
            )

    # Apply optional filters
    if filter_id:
        spec.add_specification(IdSpecification(filter_id))
    if state:
        spec.add_specification(StateSpecification(state))

    # Retrieve sessions
    sessions: list[Session] = wad.get_sessions(spec)

    # Generate output
    output_visitors = {
        OutputType.TABLE: TableVisitor(console),
        OutputType.DETAILS: DetailsVisitor(console),
    }

    visitor: ModelVisitor = output_visitors[output_type]
    for session in sessions:
        session.accept(visitor)
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
def common_command_line_options(ctx: Context, json_filename: str) -> None:
    """Default callback for the command line options.

    Will always be called before the correct command is called. This way, we
    can setup a object that is used by all commands.
    """
    ctx.obj = {
        'console': console,
        'wad': WadProgramApp(
            retriever=HtmlProgramRetriever(WebPageLoader()),
            database=JsonDatabase(json_filename=json_filename),
        ),
    }


def main() -> None:
    """Main entry point for the application.

    Will start the Typer app for the CLI arguments.
    """
    app()
