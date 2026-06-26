"""Main entry point for the CLI."""

from rich.console import Console
from rich.progress import Progress
from typer import Context, Typer

from .html_program_retriever import HtmlProgramRetriever
from .json_database import JsonDatabase
from .page_loader import WebPageLoader
from .wad_program_app import WadProgramApp

app = Typer(no_args_is_help=True)
console = Console()


@app.command(
    name='list', help='List the sessions', short_help='List the sessions'
)
def list_sessions(ctx: Context) -> None:
    """List sessions currently in the database."""
    # TODO: Implement
    pass


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

    Will always be called before the correct command is called. This way, we can
    setup a object that is used by all commands.
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
