"""Tests for the HtmlProgramRetriever class."""

from wad_program.html_program_retriever import HtmlProgramRetriever
from wad_program.page_loader import LocalFilePageLoader


def test_loading_sessions_from_html() -> None:
    """Test loading from fake HTML pages."""
    pages = [
        '5-things-in-tech-that-matter-now-2026-edition-1260805',
        'cuda-python-gpu-programming-for-the-modern-developer-1246897',
        'design-patterns-for-ai-products-in-2026-1150609',
        'how-to-read-code-properly-1085275',
        'introducing-json-structure-1119688',
        'keynote-1244226',
        'you-will-migrate-eventually-a-developer-approach-to-technology-'
        'adoption-1154249',
    ]
    base_url = 'https://www.wearedevelopers.com/world-congress/agenda/sessions'
    html_retriever = HtmlProgramRetriever(
        LocalFilePageLoader(
            main_filename='tests/test_data/program_page.html',
            session_page_filenames={
                f'{base_url}/{page}': f'tests/test_data/{page}.html'
                for page in pages
            },
        )
    )
    data = html_retriever.retrieve_program()
    assert len(data.sessions) == 7
