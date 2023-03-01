"""This file describes the functionality of adding data from a json file to the database."""
import json

from ask_me_bot.questions.exceptions import DataExportError, JsonKeysError, ThemeNotExistedError, QuestionLengthError, \
    ExplanationLengthError, AnswerLengthError, LotIncorrectAnswersError
from models import postgres_client


def parse_data_from_json(path_to_file: str) -> list[dict[str, str | dict[str, str]], ...]:
    """
    Receives as input the path to the json file containing information for the quiz in the telegram.
    Json file Example:
    {
      "data": [
        {
          "theme": "Python",
          "question": "Выберите неизменяемый тип данных",
          "explanation": "tuple - является неизменяемой структурой данных,
          "correct_answer": "tuple",
          "incorrect_answers": {
            "1": "list",
            "2": "byte arrays",
            "3": "dict"
          }
        }
      ]
    }
    :param path_to_file: 'export/questions.json'

    Returns a list of dictionaries, where each dictionary stores data about one quiz question.
    """
    with open(path_to_file) as f:
        json_load = json.load(f)
        data = [el for el in json_load['data']]

    return data


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
    insert = f"""insert into questions (theme_id, question_name, explanation) values({theme_id}, '{question}', '{explanation}') RETURNING question_id;"""
    postgres_client.cursor.execute(insert)
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
    test_data = parse_data_from_json(path_to_file='export/questions.json')
    insert_data_with_questions_to_database(test_data)
