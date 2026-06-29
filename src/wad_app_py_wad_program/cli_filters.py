"""Module with filters for the CLI commands."""

from wad_app_py_wad_program.cli_builders import SpecBuildDict
from wad_app_py_wad_program.database_specifications import (
    SessionTextContainsSpecification,
    SpeakerTextContainsSpecification,
    TopicTextContainsSpecification,
)
from wad_app_py_wad_program.model import Session, Speaker, Topic

cli_session_text_filters: SpecBuildDict[Session] = {
    'title': lambda text: SessionTextContainsSpecification(text, ['title']),
    'description': lambda text: SessionTextContainsSpecification(
        text, ['description']
    ),
    'any': lambda text: SessionTextContainsSpecification(
        text, ['title', 'description', 'stage', 'main_topic', 'topics']
    ),
    'main_topic': lambda text: SessionTextContainsSpecification(
        text, ['main_topic']
    ),
    'stage': lambda text: SessionTextContainsSpecification(text, ['stage']),
    'topic': lambda text: SessionTextContainsSpecification(text, ['topics']),
}

cli_speaker_text_filters: SpecBuildDict[Speaker] = {
    'speaker_any': lambda text: SpeakerTextContainsSpecification(
        text, ['name', 'job', 'tagline', 'summary']
    ),
    'speaker_name': lambda text: SpeakerTextContainsSpecification(
        text, ['name']
    ),
    'speaker_tagline': lambda text: SpeakerTextContainsSpecification(
        text, ['tagline']
    ),
    'speaker_job': lambda text: SpeakerTextContainsSpecification(
        text, ['job']
    ),
    'speaker_summary': lambda text: SpeakerTextContainsSpecification(
        text, ['summary']
    ),
}

cli_topics_text_filters: SpecBuildDict[Topic] = {
    'name': lambda text: TopicTextContainsSpecification(text, ['name'])
}
