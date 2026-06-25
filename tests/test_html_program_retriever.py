from wad_app_py_wad_program.html_program_retriever import HtmlProgramRetriever
from wad_app_py_wad_program.page_loader import LocalFilePageLoader


def test_loading_sessions_from_html() -> None:
    html_retriever = HtmlProgramRetriever(
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
    )
    data = html_retriever.retrieve_program()
    assert len(data.sessions) == 0
