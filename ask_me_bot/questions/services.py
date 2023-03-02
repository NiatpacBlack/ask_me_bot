"""This file contains the business logic of the question's module."""
from typing import Any
from random import choice, shuffle

from ask_me_bot.questions.models import create_themes_table, create_questions_table, create_answers_table, \
    postgres_client


def create_all_tables_for_db() -> None:
    """Create all tables for the database."""
    create_themes_table()
    create_questions_table()
    create_answers_table()


def get_all_questions_from_db() -> list[tuple[Any, ...], ...]:
    """Returns all questions from the database."""
    questions = postgres_client.select_all_from_table('questions')
    return questions


def get_random_question_from_questions(questions: list[tuple[Any, ...], ...]) -> tuple[Any, ...]:
    """Returns one random question from the list of questions."""
    question = choice(questions)
    return question


def get_sorted_answers_from_question(question: tuple[Any, ...]) -> list[Any, ...]:
    """
    Returns a list of answers to the question given to question,
    the first element of the list will always be the correct answer.
    """
    question_id = question[0]
    query = f"""select * from answers where question_id = {question_id};"""
    postgres_client.cursor.execute(query)
    answers = postgres_client.cursor.fetchall()
    return [answer[2] for answer in answers if answer[3] is True] + \
        [answer[2] for answer in answers if answer[3] is False]


def get_question_and_answers() -> tuple[str, list[str, ...], int, str]:
    """
    The function receives a random question from the database and answers to it, saves the correct answer,
    shuffles the answers, and returns a tuple with the received data.
    """

    question = get_random_question_from_questions(get_all_questions_from_db())
    answers = get_sorted_answers_from_question(question)
    correct_answer = answers[0]
    explanation = question[3]

    shuffle(answers)

    index_current_answer = [index for index, answer in enumerate(answers) if answer == correct_answer][0]

    return question[2], answers, index_current_answer, explanation


if __name__ == '__main__':
    print(get_question_and_answers())
