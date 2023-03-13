"""This file contains the business logic of the question's module."""
from dataclasses import dataclass
from datetime import datetime
from random import choice, shuffle
from typing import Any

import pytz

from ask_me_bot.config import TIME_ZONE
from ask_me_bot.questions.exceptions import DataKeysError, ThemeNotExistedError, QuestionLengthError, \
    ExplanationLengthError, AnswerLengthError, LotIncorrectAnswersError, GetQuestionWithThemeNameError, \
    GetAnswersForQuestionError, ExistingThemeError
from ask_me_bot.questions.models import postgres_client


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
    correct_answer: str
    incorrect_answers: list[str, ...]


@dataclass(slots=True, frozen=True)
class QuestionForQuiz:
    """Description of the question and answer data type for the quiz telegram bot."""

    question_name: str
    answers: list[str, ...]
    index_current_answer: int
    explanation: str


def get_themes_for_choices() -> list[tuple[str, str]]:
    """Get list of topics for SelectField in CreateQuestionForm."""
    postgres_client.cursor.execute("""select theme_id, theme_name from themes;""")
    themes = postgres_client.cursor.fetchall()
    return themes


def get_all_questions_from_db() -> list[Question, ...]:
    """Returns all questions from the database."""
    questions = postgres_client.select_all_from_table('questions')
    return [Question(*question) for question in questions]


def get_all_themes_from_db() -> list[Theme, ...]:
    """Returns all themes from the database."""
    themes = postgres_client.select_all_from_table('themes')
    return [Theme(*theme) for theme in themes]


def get_all_questions_with_theme_name_from_db() -> list[None] | list[QuestionWithThemeName, ...]:
    """Returns all questions from the database along with the topic title."""
    postgres_client.cursor.execute("""
        select question_id, theme_id, question_name, explanation, 
        questions.creation_date, questions.modification_date, theme_name
        from questions JOIN themes USING(theme_id);
        """)
    questions_with_theme_name = postgres_client.cursor.fetchall()
    return questions_with_theme_name if not questions_with_theme_name else [QuestionWithThemeName(*el) for el in
                                                                            questions_with_theme_name]


def get_random_question_from_questions(questions: list[Question, ...]) -> Question:
    """Returns one random question from the list of questions."""
    question = choice(questions)
    return question


def get_incorrect_answers_for_question(question_id: str) -> list[Answer, ...] | tuple[None]:
    """Возвращает список неправильных ответов для вопроса с question_id. """
    query = f"""select * from answers where question_id = {question_id} and is_right='false';"""
    postgres_client.cursor.execute(query)
    incorrect_answers = postgres_client.cursor.fetchall()
    return [Answer(
        answer_id=incorrect_answer[0],
        answer_name=incorrect_answer[2],
    ) for incorrect_answer in incorrect_answers] if incorrect_answers else ()


def get_correct_answer_for_question(question_id: str) -> Answer | tuple[None]:
    """Returns the correct answer for the question with question_id."""
    query = f"""select * from answers where question_id = {question_id} and is_right='true';"""
    postgres_client.cursor.execute(query)
    correct_answer = postgres_client.cursor.fetchone()
    return Answer(
        answer_id=correct_answer[0],
        answer_name=correct_answer[2],
    ) if correct_answer else ()


def get_answers_for_question(question_id: str) -> AnswersForQuestion:
    """Returns the answers for the question with question_id."""
    correct_answer = get_correct_answer_for_question(question_id)
    incorrect_answers = get_incorrect_answers_for_question(question_id)

    if correct_answer and incorrect_answers:
        answers = AnswersForQuestion(
            correct_answer=correct_answer,
            incorrect_answers=incorrect_answers,
        )
        return answers
    raise GetAnswersForQuestionError(f"Unable to get answer data for question with id {question_id}.")


def parse_request_data_to_question_format(request_data: dict[Any, ...]) -> QuestionForDatabase:
    """Converts a dictionary of question data into a format suitable for adding the question to the database."""
    dict_incorrect_answers = {key[-1]: value for key, value in request_data.items() if
                              'incorrect_answer' in key and value and key != 'incorrect_answers_id'}

    return QuestionForDatabase(
        theme_id=request_data["theme_id"],
        question=request_data["question"],
        explanation=request_data["explanation"],
        correct_answer=request_data["correct_answer"],
        incorrect_answers=[answer for answer in dict_incorrect_answers.values()]
    )


def parse_request_data_to_theme_format(request_data: dict[Any, ...]) -> dict[str, str]:
    return {
        "theme_name": request_data["theme_name"],
    }


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
        select question_id, theme_id, question_name, explanation,
        questions.creation_date, questions.modification_date, theme_name
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


def get_theme_id_from_theme_name(theme_name: str) -> int | None:
    """Returns the id of the theme from the database whose name is passed to theme_name."""
    query = f"""select theme_id from themes where theme_name = '{theme_name}';"""
    postgres_client.cursor.execute(query)
    theme_id = postgres_client.cursor.fetchone()
    return theme_id[0] if theme_id else None


def insert_question_in_questions_table(theme_id: str, question: str, explanation: str) -> int:
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


def update_question_in_questions_table(theme_id: str, question_id: str, question: str, explanation: str) -> None:
    """
    Updates a question subject, question, and answer explanation to the question table in the database.
    Returns the id of the updated question.
    """
    query = f"""
        update questions set(theme_id, question_name, explanation, modification_date)=(
            {theme_id}, '{question}', '{explanation}', '{datetime.now(pytz.timezone(TIME_ZONE))}'
            )
        WHERE question_id = {question_id}     
        RETURNING question_id;
        """
    postgres_client.cursor.execute(query)
    postgres_client.db_connect.commit()


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
        insert = f"""
            insert into answers (question_id, answer_name, is_right) 
            values({question_id}, '{answer}', {"true" if index == 1 else "false"})
            """
        postgres_client.cursor.execute(insert)
        postgres_client.db_connect.commit()


def insert_theme_in_themes_table(theme_name: str) -> str:
    """Add a theme to the themes table in the database."""
    query = f"""
    insert into themes (theme_name, creation_date) 
    values('{theme_name}', '{datetime.now(pytz.timezone(TIME_ZONE))}')
    returning theme_id;
    """
    postgres_client.cursor.execute(query)
    theme_id = postgres_client.cursor.fetchone()
    postgres_client.db_connect.commit()
    return str(theme_id[0])


def update_answers_for_question(
        correct_answer_id: str,
        incorrect_answers_id: list[str, ...],
        correct_answer: str,
        incorrect_answers: list[str, ...]
) -> None:
    """Updates the answers to the question with question_id in the answer table in the database."""
    update_correct_answer_query = f"""
        update answers set answer_name='{correct_answer}'
        where answer_id = {correct_answer_id};
        """
    postgres_client.cursor.execute(update_correct_answer_query)
    postgres_client.db_connect.commit()
    for index, incorrect_answer in enumerate(incorrect_answers, 0):
        update_incorrect_answer_query = f"""
            update answers set answer_name='{incorrect_answer}'
            where answer_id = {incorrect_answers_id[index]};
            """
        postgres_client.cursor.execute(update_incorrect_answer_query)
        postgres_client.db_connect.commit()


def insert_data_with_questions_to_database(data: list[QuestionForDatabase, ...]) -> None:
    """Adds submitted data related to quiz questions to database tables."""
    for question in data:
        _validate_question_data(question)
        if not get_question_id_from_question_name(question_name=question.question):
            question_id = insert_question_in_questions_table(question.theme_id, question.question, question.explanation)
            insert_answers_for_question(question_id, question.correct_answer, question.incorrect_answers)


def insert_data_with_theme_to_database(data: dict[str, str]) -> str:
    """Adds data about a topic to the database."""
    _validate_theme_data(data)
    theme_id = insert_theme_in_themes_table(data['theme_name'])
    return theme_id


def update_question_in_database(
        data: QuestionForDatabase,
        question_id: str,
        correct_answer_id: str,
        incorrect_answers_id: list[str, ...]
) -> None:
    """Updates the question and its answers in the database by changing the fields passed to data."""
    _validate_question_data(data)
    update_question_in_questions_table(data.theme_id, question_id, data.question, data.explanation)
    update_answers_for_question(correct_answer_id, incorrect_answers_id, data.correct_answer,
                                data.incorrect_answers)


def delete_question_from_database(question_id: str) -> None:
    """Deletes the question with question_id from the database."""
    postgres_client.delete_value_in_table('questions', f'question_id = {int(question_id)}')


def _validate_question_data(data: QuestionForDatabase) -> None:
    """Performs checks on all fields in the received data, returns QuestionForDatabase."""
    try:
        _question_validation(data.question),
        _explanation_validation(data.explanation),
        _correct_answer_validation(data.correct_answer),
        _incorrect_answers_validation(data.incorrect_answers)
    except KeyError:
        raise DataKeysError("Invalid input data, you need to pass data with fields corresponding to the quiz question.")


def _validate_theme_data(data: dict[str, str]) -> None:
    try:
        if get_theme_id_from_theme_name(theme_name=data['theme_name']):
            raise ExistingThemeError("A theme with the same name already exists.")
    except KeyError:
        raise DataKeysError("Invalid input data, you need to pass data with fields corresponding to the theme")


def _theme_validation(theme_name: str) -> None:
    """Question Topic Title Check: Checks for the existence of such a topic in the database."""
    if not get_theme_id_from_theme_name(theme_name=theme_name):
        raise ThemeNotExistedError(
            f"Theme with this name does not exist in the database, "
            f"create it or check the entered data. Incorrect theme: {theme_name}"
        )


def _question_validation(question: str) -> None:
    """
    Checking the question:
    Question must not exceed 255 characters in length. Restriction of the form of a quiz in a telegram.
    """
    if len(question) > 255:
        raise QuestionLengthError(
            f"The length of the question should not exceed 255 characters. "
            f"Check input received from json. Incorrect question: {question}"
        )


def _explanation_validation(explanation: str) -> None:
    """
    Checking the explanation:
    Explanation must not exceed 200 characters in length. Restriction of the form of a quiz in a telegram.
    """
    if len(explanation) > 200:
        raise ExplanationLengthError(
            f"The length of the explanation should not exceed 200 characters. "
            f"Check input received from json. Incorrect explanation: {explanation}"
        )


def _correct_answer_validation(correct_answer: str) -> None:
    """
    Checking the correct answer:
    Answer must not exceed 100 characters in length. Restriction of the form of a quiz in a telegram.
    """
    if len(correct_answer) > 100:
        raise AnswerLengthError(
            f"The length of the correct answer should not exceed 100 characters. "
            f"Check input received from json. Incorrect answer: {correct_answer}"
        )


def _incorrect_answers_validation(incorrect_answers: list[str, ...]) -> None:
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


if __name__ == '__main__':
    from ask_me_bot.questions.converter import parse_data_from_json
    test_data = parse_data_from_json(path_to_file='export/questions.json')
    insert_data_with_questions_to_database(test_data)
