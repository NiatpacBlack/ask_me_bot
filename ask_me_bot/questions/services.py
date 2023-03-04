"""This file contains the business logic of the question's module."""
from dataclasses import dataclass
from datetime import datetime
from random import choice, shuffle

import pytz

from ask_me_bot.config import TIME_ZONE
from ask_me_bot.questions.models import create_themes_table, create_questions_table, create_answers_table, \
    postgres_client
from ask_me_bot.questions.exceptions import DataExportError, JsonKeysError, ThemeNotExistedError, QuestionLengthError, \
    ExplanationLengthError, AnswerLengthError, LotIncorrectAnswersError, GetQuestionWithThemeNameError, \
    GetAnswersForQuestionError


@dataclass(slots=True, frozen=True)
class Question:
    """Description of the question data type."""

    question_id: int
    theme_id: int
    question_name: str
    explanation: str
    creation_date: datetime
    modification_date: datetime


@dataclass(slots=True, frozen=True)
class Answer:
    """Data type description of the answers for question."""

    correct_answer: str
    incorrect_answers: list[str, ...]


@dataclass(slots=True, frozen=True)
class QuestionWithThemeName(Question):
    """Description of the question data type."""

    theme_name: str


@dataclass(slots=True, frozen=True)
class QuestionForQuiz:
    """Description of the question and answer data type for the quiz telegram bot."""

    question_name: str
    answers: list[str, ...]
    index_current_answer: int
    explanation: str


def create_all_tables_for_db() -> None:
    """Create all tables for the database."""
    create_themes_table()
    create_questions_table()
    create_answers_table()


def get_all_questions_from_db() -> list[Question, ...]:
    """Returns all questions from the database."""
    questions = postgres_client.select_all_from_table('questions')
    return [Question(*question) for question in questions]


def get_all_questions_with_theme_name_from_db() -> list[None] | list[QuestionWithThemeName, ...]:
    """Returns all questions from the database along with the topic title."""
    postgres_client.cursor.execute("""
        select question_id, theme_id, question_name, explanation, creation_date, modification_date, theme_name
        from questions JOIN themes USING(theme_id);
        """)
    questions_with_theme_name = postgres_client.cursor.fetchall()
    return questions_with_theme_name if not questions_with_theme_name else [QuestionWithThemeName(*el) for el in
                                                                            questions_with_theme_name]


def get_random_question_from_questions(questions: list[Question, ...]) -> Question:
    """Returns one random question from the list of questions."""
    question = choice(questions)
    return question


def get_incorrect_answers_for_question(question_id: str) -> list[str, ...] | tuple[None]:
    """Возвращает список неправильных ответов для вопроса с question_id. """
    query = f"""select * from answers where question_id = {question_id} and is_right='false';"""
    postgres_client.cursor.execute(query)
    incorrect_answers = postgres_client.cursor.fetchall()
    return [answer[2] for answer in incorrect_answers] if incorrect_answers else ()


def get_correct_answer_for_question(question_id: str) -> str | tuple[None]:
    """Возвращает правильный ответ для вопроса с question_id. """
    query = f"""select * from answers where question_id = {question_id} and is_right='true';"""
    postgres_client.cursor.execute(query)
    correct_answer = postgres_client.cursor.fetchone()
    return correct_answer[2] if correct_answer else ()


def get_answers_for_question(question_id: str) -> Answer:
    """Returns the answers for the question with question_id."""
    correct_answer = get_correct_answer_for_question(question_id)
    incorrect_answers = get_incorrect_answers_for_question(question_id)

    if correct_answer and incorrect_answers:
        answers = Answer(
            correct_answer=correct_answer,
            incorrect_answers=incorrect_answers,
        )
        return answers
    raise GetAnswersForQuestionError(f"Unable to get answer data for question with id {question_id}.")


def get_sorted_answers_from_question(question: Question) -> list[str, ...]:
    """
    Returns a list of answers to the question given to question,
    the first element of the list will always be the correct answer.
    """
    query = f"""select * from answers where question_id = {question.question_id};"""
    postgres_client.cursor.execute(query)
    answers = postgres_client.cursor.fetchall()
    return [answer[2] for answer in answers if answer[3] is True] + \
        [answer[2] for answer in answers if answer[3] is False]


def get_question_with_theme_name(question_id: str) -> QuestionWithThemeName:
    query = f"""
        select question_id, theme_id, question_name, explanation, creation_date, modification_date, theme_name
        from questions join themes using(theme_id) 
        where question_id = {question_id};
        """
    postgres_client.cursor.execute(query)
    if question := postgres_client.cursor.fetchone():
        question = QuestionWithThemeName(*question)
        return question
    raise GetQuestionWithThemeNameError("Failed to get question and question subject data.")


def get_question_and_answers() -> QuestionForQuiz:
    """
    The function receives a random question from the database and answers to it, saves the correct answer,
    shuffles the answers, and returns a tuple with the received data.
    """

    question = get_random_question_from_questions(get_all_questions_from_db())
    answers = get_sorted_answers_from_question(question)
    correct_answer = answers[0]

    shuffle(answers)

    index_current_answer = [index for index, answer in enumerate(answers) if answer == correct_answer][0]

    return QuestionForQuiz(question.question_name, answers, index_current_answer, question.explanation)


def get_theme_id_from_theme_name(theme_name: str) -> int:
    """Returns the id of the theme from the database whose name is passed to theme_name."""
    query = f"""select theme_id from themes where theme_name = '{theme_name}';"""
    postgres_client.cursor.execute(query)
    theme_id = postgres_client.cursor.fetchone()[0]
    return theme_id


def insert_question_in_questions_table(theme_id: int, question: str, explanation: str) -> int:
    """
    Adds a question subject, question, and answer explanation to the question table in the database.
    Returns the id of the added question.
    """
    query = f"""
        insert into questions (theme_id, question_name, explanation, creation_date) 
        values({theme_id}, '{question}', '{explanation}', '{datetime.now(pytz.timezone(TIME_ZONE))}') 
        RETURNING question_id;
        """
    postgres_client.cursor.execute(query)
    question_id = postgres_client.cursor.fetchone()
    postgres_client.db_connect.commit()
    return question_id[0]


def get_question_id_from_question_name(question_name: str) -> int | bool:
    """Returns the question id from the database where the question name matches question_name."""
    query = f"""select question_id from questions where question_name = '{question_name}';"""
    postgres_client.cursor.execute(query)
    result = postgres_client.cursor.fetchone()
    return result[0] if result else False


def insert_answers_for_question(question_id: int, correct_answer: str, incorrect_answers: list[str, ...]) -> None:
    """
    Adds the answers to the question with question_id to the answer table in the database.
    The function accepts correct and incorrect answers,
    placing the correct answer at the beginning of the list of answers.
    """
    answers = [correct_answer]
    answers.extend(incorrect_answers)
    for index, answer in enumerate(answers, 1):
        insert = f"""insert into answers (question_id, answer_name, is_right) values({question_id}, '{answer}', {"true" if index == 1 else "false"})"""
        postgres_client.cursor.execute(insert)
        postgres_client.db_connect.commit()


def insert_data_with_questions_to_database(data: list[dict[str, str | dict[str, str]], ...]) -> None:
    """Adds submitted data related to quiz questions to database tables."""
    try:
        for dictionary in data:
            try:
                theme: str = _theme_validation(dictionary["theme"])
                question: str = _question_validation(dictionary["question"])
                explanation: str = _explanation_validation(dictionary["explanation"])
                correct_answer: str = _correct_answer_validation(dictionary["correct_answer"])
                incorrect_answers: list[str, ...] = _incorrect_answers_validation(
                    [answer for answer in dictionary["incorrect_answers"].values()]
                )
            except KeyError:
                raise JsonKeysError("Invalid data received as input from json file.")

            theme_id = get_theme_id_from_theme_name(theme_name=theme)
            if not get_question_id_from_question_name(question_name=question):
                question_id = insert_question_in_questions_table(theme_id, question, explanation)
                insert_answers_for_question(
                    question_id,
                    correct_answer,
                    incorrect_answers,
                )
    except Exception as e:
        raise DataExportError(f"An unexpected error occurred while trying to export data to the database. Info: {e}")


def _theme_validation(theme_name: str) -> str:
    """Question Topic Title Check: Checks for the existence of such a topic in the database."""
    if not get_theme_id_from_theme_name(theme_name=theme_name):
        raise ThemeNotExistedError(
            f"Theme with this name does not exist in the database, "
            f"create it or check the entered data. Incorrect theme: {theme_name}"
        )
    return theme_name


def _question_validation(question: str) -> str:
    """
    Checking the question:
    Question must not exceed 255 characters in length. Restriction of the form of a quiz in a telegram.
    """
    if len(question) > 255:
        raise QuestionLengthError(
            f"The length of the question should not exceed 255 characters. "
            f"Check input received from json. Incorrect question: {question}"
        )
    return question


def _explanation_validation(explanation: str) -> str:
    """
    Checking the explanation:
    Explanation must not exceed 200 characters in length. Restriction of the form of a quiz in a telegram.
    """
    if len(explanation) > 200:
        raise ExplanationLengthError(
            f"The length of the explanation should not exceed 200 characters. "
            f"Check input received from json. Incorrect explanation: {explanation}"
        )
    return explanation


def _correct_answer_validation(correct_answer: str) -> str:
    """
    Checking the correct answer:
    Answer must not exceed 100 characters in length. Restriction of the form of a quiz in a telegram.
    """
    if len(correct_answer) > 100:
        raise AnswerLengthError(
            f"The length of the correct answer should not exceed 100 characters. "
            f"Check input received from json. Incorrect answer: {correct_answer}"
        )
    return correct_answer


def _incorrect_answers_validation(incorrect_answers: list[str, ...]) -> list[str, ...]:
    """
    Checking the list of incorrect answers:
    Each answer must not exceed 100 characters in length. Restriction of the form of a quiz in a telegram.
    Questions should not be more than 9. Restriction of the quiz form in the telegram.
    """
    if len(incorrect_answers) > 9:
        raise LotIncorrectAnswersError(
            f"Too many incorrect answers passed, there should not be more than 9. "
            f"Check the data passed from json. Incorrect Answers: {incorrect_answers}"
        )
    for answer in incorrect_answers:
        if len(answer) > 100:
            raise AnswerLengthError(
                f"The length of the correct answer should not exceed 100 characters. "
                f"Check input received from json. Incorrect answer: {answer}"
            )
    return incorrect_answers


if __name__ == '__main__':
    from ask_me_bot.questions.converter import parse_data_from_json
    create_all_tables_for_db()
    test_data = parse_data_from_json(path_to_file='export/questions.json')
    insert_data_with_questions_to_database(test_data)
