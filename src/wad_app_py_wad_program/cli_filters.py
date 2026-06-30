"""Module with filters for the CLI commands."""

from datetime import datetime

from wad_app_py_wad_program.database_specifications import (
    ComparisonOperator,
    FieldComparisonOperatorSpecification,
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

from .filter_specifications import FilterSpecifications

session_filters = FilterSpecifications[Session](
    text={
        'title': lambda text: SessionTextContainsSpecification(
            text, ['title']
        ),
        'description': lambda text: SessionTextContainsSpecification(
            text, ['description']
        ),
        'any': lambda text: SessionTextContainsSpecification(
            text, ['title', 'description', 'stage', 'main_topic', 'topics']
        ),
        'main_topic': lambda text: SessionTextContainsSpecification(
            text, ['main_topic']
        ),
        'stage': lambda text: SessionTextContainsSpecification(
            text, ['stage']
        ),
        'topic': lambda text: SessionTextContainsSpecification(
            text, ['topics']
        ),
    },
    comparison={
        'filter_id': lambda value: FieldComparisonOperatorSpecification(
            value, 'id', ComparisonOperator.EQUALS
        ),
        'state': lambda value: FieldComparisonOperatorSpecification(
            SessionState(value), 'state', ComparisonOperator.EQUALS
        ),
        'interest_level': lambda value: FieldComparisonOperatorSpecification(
            InterestLevel(value), 'interest_level', ComparisonOperator.EQUALS
        ),
        'day': lambda value: FieldComparisonOperatorSpecification(
            Day(value), 'day', ComparisonOperator.EQUALS
        ),
        'start_time_after': lambda value: FieldComparisonOperatorSpecification(
            datetime.strptime(value, '%H:%M').time(),
            'start_time_time',
            ComparisonOperator.LE,
        ),
        'end_time_before': lambda value: FieldComparisonOperatorSpecification(
            datetime.strptime(value, '%H:%M').time(),
            'end_time_time',
            ComparisonOperator.GE,
        ),
    },
)

session_speaker_filters = FilterSpecifications[Speaker](
    text={
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
)

topic_filters = FilterSpecifications[Topic](
    text={'name': lambda text: TopicTextContainsSpecification(text, ['name'])},
    comparison={
        'main_topic': lambda value: FieldComparisonOperatorSpecification(
            bool(value), 'is_main_topic', ComparisonOperator.EQUALS
        ),
    },
)
