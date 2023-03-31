"""This file stores all data classes created for convenient work with project data."""
from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True, frozen=True)
class Question:
    """Description of the question data type."""

    question_id: int
    theme_id: int
    question_name: str
    explanation: str
    detail_explanation: str
    creation_date: datetime
    modification_date: datetime


@dataclass(slots=True, frozen=True)
class Answer:
    """Data type description of the answers for question."""

    answer_id: int
    answer_name: str


@dataclass(slots=True, frozen=True)
class Theme:
    """Data type description of the theme."""

    theme_id: int
    theme_name: str
    creation_date: datetime
    modification_date: datetime


@dataclass(slots=True, frozen=True)
class AnswersForQuestion:
    """Data type description of the answers for question."""

    correct_answer: Answer
    incorrect_answers: list[Answer, ...]


@dataclass(slots=True, frozen=True)
class QuestionWithThemeName(Question):
    """Description of the question data type."""

    theme_name: str


@dataclass(slots=True, frozen=True)
class QuestionForDatabase:
    """Description of the question data type for adding to database."""

    theme_id: str
    question: str
    explanation: str
    detail_explanation: str
    correct_answer: str
    incorrect_answers: list[str, ...]


@dataclass(slots=True, frozen=True)
class QuestionForQuiz:
    """Description of the question and answer data type for the quiz telegram bot."""

    question_name: str
    answers: list[str, ...]
    index_current_answer: int
    explanation: str
