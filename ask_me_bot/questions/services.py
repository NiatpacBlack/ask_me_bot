"""This file contains the business logic of the question's module."""
from models import create_themes_table, create_questions_table, create_answers_table


def create_all_tables_for_db() -> None:
    """Create all tables for the database."""
    create_themes_table()
    create_questions_table()
    create_answers_table()


if __name__ == '__main__':
    create_all_tables_for_db()
