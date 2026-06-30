"""Module with filters for the CLI commands."""

from wad_app_py_wad_program.cli_builders import (
    EqualitySpecBuildDict,
    TextContainsSpecBuildDict,
)
from wad_app_py_wad_program.database_specifications import (
    FieldIsEqualToSpecification,
    SessionTextContainsSpecification,
    SpeakerTextContainsSpecification,
    TopicTextContainsSpecification,
)
from wad_app_py_wad_program.model import (
    Day,
    InterestLevel,
    Session,
    SessionState,
    Speaker,
    Topic,
)

cli_session_text_filters: TextContainsSpecBuildDict[Session] = {
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

cli_session_equality_filters: EqualitySpecBuildDict[Session] = {
    'filter_id': lambda value: FieldIsEqualToSpecification(value, 'id', int),
    'state': lambda value: FieldIsEqualToSpecification(
        SessionState(value), 'state', SessionState
    ),
    'interest_level': lambda value: FieldIsEqualToSpecification(
        InterestLevel(value), 'interest_level', InterestLevel
    ),
    'day': lambda value: FieldIsEqualToSpecification(Day(value), 'day', Day),
}

cli_speaker_text_filters: TextContainsSpecBuildDict[Speaker] = {
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

cli_topics_text_filters: TextContainsSpecBuildDict[Topic] = {
    'name': lambda text: TopicTextContainsSpecification(text, ['name'])
}

cli_topics_equality_filters: EqualitySpecBuildDict[Topic] = {
    'main_topic': lambda value: FieldIsEqualToSpecification(
        bool(value), 'is_main_topic', bool
    ),
}
