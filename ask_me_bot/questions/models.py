"""This file describes the tables of questions, answers and topics."""
from ask_me_bot.config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST
from ask_me_bot.db_client.db import PostgresClient


postgres_client = PostgresClient(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
)


def create_themes_table() -> None:
    """Creates the themes table, which will contain the names of the topics for questions."""

    postgres_client.create_table(
        "themes",
        "theme_id SERIAL PRIMARY KEY, theme_name VARCHAR(255) NOT NULL",
    )


def create_questions_table() -> None:
    """
    Creates the questions table, which will contain questions on the topic and an explanation of the answer.
    The question is related to a specific theme from the themes table.
    """

    postgres_client.create_table(
        "questions",
        """
        question_id SERIAL PRIMARY KEY,
        theme_id INTEGER NOT NULL,
        question_name TEXT NOT NULL,
        explanation TEXT NULL,
        FOREIGN KEY (theme_id) REFERENCES themes (theme_id) ON DELETE CASCADE
        """,
    )


def create_answers_table() -> None:
    """
    Creates an answer table that contains answers to a specific question from the questions table.

    Answers can be right (is_right = True) or wrong (is_right = False)
    """

    postgres_client.create_table(
        "answers",
        """
        answer_id SERIAL PRIMARY KEY,
        question_id INTEGER NOT NULL,
        answer_name TEXT NOT NULL,
        is_right BOOLEAN NOT NULL,
        FOREIGN KEY (question_id) REFERENCES questions (question_id) ON DELETE CASCADE
        """,
    )
