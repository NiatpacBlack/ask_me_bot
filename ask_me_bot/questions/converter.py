"""This file describes the functionality of parsing and adding data to json file."""
import json
import traceback
from datetime import datetime

from ask_me_bot.config import EXPORT_PATH, logger
from ask_me_bot.questions.exceptions import JsonIncorrectData
from ask_me_bot.questions.services import QuestionForDatabase, get_theme_id_from_theme_name, \
    insert_data_with_theme_to_database


def add_data_to_json_file(data: dict[str, str, str, str, dict[str, str]]) -> None:
    """Appends the passed data to the json file."""

    filename = f"questions_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.json"

    with open(EXPORT_PATH + filename, mode='w', encoding='utf-8') as file:
        json.dump(data, file)


def parse_data_from_json(path_to_file: str) -> list[QuestionForDatabase, ...]:
    """
    Receives as input the path to the json file containing information for the quiz in the telegram.
    Json file Example:
    {
      "data": [
        {
          "theme": "Python",
          "question": "Choose an immutable data type",
          "explanation": "tuple - is an immutable data structure",
          "correct_answer": "tuple",
          "detail_explanation: "this is an optional parameter",
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
    The json data format was created specifically for entering information without knowing about the theme id
    or other data from the database.
    """
    with open(path_to_file, encoding='utf-8') as file:
        json_load = json.load(file)
        data = []
        for question in json_load['data']:
            try:
                theme_id = get_theme_id_from_theme_name(theme_name=question['theme'])
                result = QuestionForDatabase(
                    theme_id=theme_id if theme_id else insert_data_with_theme_to_database(
                        data={'theme_name': question['theme']}
                    ),
                    question=question['question'],
                    explanation=question['explanation'],
                    detail_explanation=question.get('detail_explanation', ""),
                    correct_answer=question['correct_answer'],
                    incorrect_answers=[answer for answer in question['incorrect_answers'].values()],
                )
            except Exception as e:
                error_message = 'The data passed in the json file is incorrect, ' \
                                f'check the data against the documentation format. Info: {e}'
                logger.exception(error_message)
                logger.error(traceback.format_exc())
                raise JsonIncorrectData(error_message)

            data.append(result)

    return data
