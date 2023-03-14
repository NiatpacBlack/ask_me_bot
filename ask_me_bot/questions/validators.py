"""This file contains all the logic for checking fields for correct input."""
from ask_me_bot.questions.dataclasses import QuestionForDatabase
from ask_me_bot.questions.exceptions import AnswerLengthError, LotIncorrectAnswersError, ExplanationLengthError, \
    QuestionLengthError, ExistingThemeError, DataKeysError


def validate_question_data(data: QuestionForDatabase) -> None:
    """Performs checks on all fields in the received data, returns QuestionForDatabase."""
    try:
        _question_validation(data.question),
        _explanation_validation(data.explanation),
        _correct_answer_validation(data.correct_answer),
        _incorrect_answers_validation(data.incorrect_answers)
    except KeyError:
        raise DataKeysError("Invalid input data, you need to pass data with fields corresponding to the quiz question.")


def validate_theme_data(data: dict[str, str]) -> None:
    from ask_me_bot.questions.services import get_theme_id_from_theme_name
    try:
        if get_theme_id_from_theme_name(theme_name=data['theme_name']):
            raise ExistingThemeError("A theme with the same name already exists.")
    except KeyError:
        raise DataKeysError("Invalid input data, you need to pass data with fields corresponding to the theme")


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
