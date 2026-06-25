"""Main entry point for the CLI."""

from typer import Context, Typer

from .html_program_retriever import HtmlProgramRetriever
from .json_database import JsonDatabase
from .page_loader import LocalFilePageLoader, WebPageLoader
from .wad_program_app import WadProgramApp

app = Typer(no_args_is_help=True)


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
    ctx.obj.update_database()


@app.callback()
def common_command_line_options(ctx: Context, json_filename: str) -> None:
    """Default callback for the command line options.

    Will always be called before the correct command is called. This way, we can
    setup a object that is used by all commands.
    """
    ctx.obj = WadProgramApp(
        retriever=HtmlProgramRetriever(WebPageLoader()),
        database=JsonDatabase(json_filename=json_filename),
    )


def main() -> None:
    """Main entry point for the application.

    Will start the Typer app for the CLI arguments.
    """
    app()
