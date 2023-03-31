"""This file contains all the logic for checking fields for correct input."""
import traceback

from ask_me_bot.questions.dataclasses import QuestionForDatabase
from ask_me_bot.questions.exceptions import AnswerLengthError, LotIncorrectAnswersError, ExplanationLengthError, \
    QuestionLengthError, ExistingThemeError, DataKeysError, DetailExplanationLengthError
from ask_me_bot.config import logger


def validate_question_data(data: QuestionForDatabase) -> None:
    """Performs checks on all fields in the received data, returns QuestionForDatabase."""
    try:
        _question_validation(data.question),
        _explanation_validation(data.explanation),
        _detail_explanation_validation(data.detail_explanation),
        _correct_answer_validation(data.correct_answer),
        _incorrect_answers_validation(data.incorrect_answers)
    except KeyError:
        error_message = "Invalid input data, you need to pass data with fields corresponding to the quiz question."
        logger.exception(error_message)
        logger.error(traceback.format_exc())
        raise DataKeysError(error_message)


def validate_theme_data(data: dict[str, str]) -> None:
    from ask_me_bot.questions.services import get_theme_id_from_theme_name
    try:
        if get_theme_id_from_theme_name(theme_name=data['theme_name']):
            raise ExistingThemeError("A theme with the same name already exists.")
    except KeyError:
        error_message = "Invalid input data, you need to pass data with fields corresponding to the theme"
        logger.exception(error_message)
        logger.error(traceback.format_exc())
        raise DataKeysError(error_message)


def _question_validation(question: str) -> None:
    """
    Checking the question:
    Question must not exceed 255 characters in length. Restriction of the form of a quiz in a telegram.
    """
    if len(question) > 255:
        error_message = f"The length of the question should not exceed 255 characters. " \
                        f"Incorrect question: {question}"
        logger.exception(error_message)
        logger.error(traceback.format_exc())
        raise QuestionLengthError(error_message)


def _explanation_validation(explanation: str) -> None:
    """
    Checking the explanation:
    Explanation must not exceed 200 characters in length. Restriction of the form of a quiz in a telegram.
    """
    if len(explanation) > 200:
        error_message = "The length of the explanation should not exceed 200 characters. " \
                        f"Incorrect explanation: {explanation}"
        logger.exception(error_message)
        logger.error(traceback.format_exc())
        raise ExplanationLengthError(error_message)


def _detail_explanation_validation(explanation: str) -> None:
    """
    Checking the detail_explanation:
    Explanation must not exceed 1024 characters in length. Restriction of the message in a telegram.
    """
    if len(explanation) > 1024:
        error_message = "The length of the detail explanation should not exceed 4096 characters. " \
                        f"Incorrect explanation: {explanation}"
        logger.exception(error_message)
        logger.error(traceback.format_exc())
        raise DetailExplanationLengthError(error_message)


def _correct_answer_validation(correct_answer: str) -> None:
    """
    Checking the correct answer:
    Answer must not exceed 100 characters in length. Restriction of the form of a quiz in a telegram.
    """
    if len(correct_answer) > 100:
        error_message = "The length of the correct answer should not exceed 100 characters. " \
                        f"Incorrect answer: {correct_answer}"
        logger.exception(error_message)
        logger.error(traceback.format_exc())
        raise AnswerLengthError(error_message)


def _incorrect_answers_validation(incorrect_answers: list[str, ...]) -> None:
    """
    Checking the list of incorrect answers:
    Each answer must not exceed 100 characters in length. Restriction of the form of a quiz in a telegram.
    Questions should not be more than 9. Restriction of the quiz form in the telegram.
    """
    if len(incorrect_answers) > 9:
        error_message = "Too many incorrect answers passed, there should not be more than 9. " \
                        f"Incorrect Answers: {incorrect_answers}"
        logger.exception(error_message)
        logger.error(traceback.format_exc())
        raise LotIncorrectAnswersError(error_message)
    for answer in incorrect_answers:
        if len(answer) > 100:
            error_message = "The length of the correct answer should not exceed 100 characters. " \
                            f"Incorrect answer: {answer}"
            logger.exception(error_message)
            logger.error(traceback.format_exc())
            raise AnswerLengthError(error_message)
