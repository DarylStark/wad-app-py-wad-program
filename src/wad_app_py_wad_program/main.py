from typer import Context, Typer

from .html_program_retriever import HtmlProgramRetriever
from .json_database import JsonDatabase
from .page_loader import LocalFilePageLoader
from .wad_program_app import WadProgramApp

app = Typer(no_args_is_help=True)


@app.command(
    name='list', help='List the sessions', short_help='List the sessions'
)
def list_sessions() -> None:
    print('Listing')


@app.command(
    name='update', help='Update the sessions', short_help='Update the sessions'
)
def update(
    ctx: Context,
) -> None:
    ctx.obj.update_database()


@app.callback()
def common_command_line_options(ctx: Context, json_filename: str) -> None:
    ctx.obj = WadProgramApp(
        retriever=HtmlProgramRetriever(
            LocalFilePageLoader(
                main_filename='tests/test_data/program_page.html',
                session_page_filenames={
                    'https://www.wearedevelopers.com/world-congress/agenda/sessions/5-things-in-tech-that-matter-now-2026-edition-1260805': 'tests/test_data/5-things-in-tech-that-matter-now-2026-edition-1260805.html',
                    'https://www.wearedevelopers.com/world-congress/agenda/sessions/cuda-python-gpu-programming-for-the-modern-developer-1246897': 'tests/test_data/cuda-python-gpu-programming-for-the-modern-developer-1246897.html',
                    'https://www.wearedevelopers.com/world-congress/agenda/sessions/design-patterns-for-ai-products-in-2026-1150609': 'tests/test_data/design-patterns-for-ai-products-in-2026-1150609.html',
                    'https://www.wearedevelopers.com/world-congress/agenda/sessions/how-to-read-code-properly-1085275': 'tests/test_data/how-to-read-code-properly-1085275.html',
                    'https://www.wearedevelopers.com/world-congress/agenda/sessions/introducing-json-structure-1119688': 'tests/test_data/introducing-json-structure-1119688.html',
                    'https://www.wearedevelopers.com/world-congress/agenda/sessions/keynote-1244226': 'tests/test_data/keynote-1244226.html',
                },
            )
        ),
        database=JsonDatabase(json_filename=json_filename),
    )


def main() -> None:
    app()
