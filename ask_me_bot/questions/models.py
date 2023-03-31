"""This file describes the tables of questions, answers and topics."""
from ask_me_bot.config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST
from ask_me_bot.db_client.db import PostgresClient


postgres_client = PostgresClient(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
)


def create_groups_table() -> None:
    """Creates a topic group table that contains the name of the group."""

    postgres_client.create_table(
        "groups",
        """
        group_id SERIAL PRIMARY KEY, 
        group_name VARCHAR(255) NOT NULL
        """
    )


def create_themes_table() -> None:
    """Creates the themes table, which will contain the names of the topics for questions."""

    postgres_client.create_table(
        "themes",
        """
        theme_id SERIAL PRIMARY KEY, 
        theme_name VARCHAR(255) NOT NULL,
        creation_date timestamp with time zone NOT NULL,
        modification_date timestamp with time zone NULL
        """
    )


def create_themes_groups_table() -> None:
    """Creates a "many to many" table to link groups to topics."""

    postgres_client.create_table(
        "themes_groups",
        """
        group_id INTEGER REFERENCES groups (group_id),
        theme_id INTEGER REFERENCES themes (theme_id),
        PRIMARY KEY (group_id, theme_id)
        """
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
        question_name VARCHAR(255) NOT NULL,
        explanation VARCHAR(200) NULL,
        detail_explanation VARCHAR(1020) NULL,
        creation_date timestamp with time zone NOT NULL,
        modification_date timestamp with time zone NULL,
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
        answer_name VARCHAR(100) NOT NULL,
        is_right BOOLEAN NOT NULL,
        FOREIGN KEY (question_id) REFERENCES questions (question_id) ON DELETE CASCADE
        """,
    )


def create_all_tables_for_db() -> None:
    """Create all tables for the database."""
    create_groups_table()
    create_themes_table()
    create_themes_groups_table()
    create_questions_table()
    create_answers_table()


if __name__ == '__main__':
    create_all_tables_for_db()
