"""This file describes the functionality of parsing and adding data to json file."""
import json

from ask_me_bot.config import EXPORT_PATH
from ask_me_bot.questions.exceptions import JsonIncorrectData
from ask_me_bot.questions.services import QuestionForDatabase, get_theme_id_from_theme_name, \
    insert_data_with_theme_to_database


def add_data_to_json_file(new_data: dict[str, str, str, str, dict[str, str]]) -> None:
    """Appends the passed data to the json file."""
    with open(EXPORT_PATH, mode='r+', encoding='utf-8') as file:
        data = json.load(file)
        if data.get('data', False):
            data["data"].append(new_data)
        else:
            data["data"] = {}
        json.dump(data, file)


def parse_data_from_json(path_to_file: str) -> list[QuestionForDatabase, ...]:
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
    The json data format was created specifically for entering information without knowing about the theme id
    or other data from the database.
    """
    with open(path_to_file) as f:
        json_load = json.load(f)
        data = []
        for el in json_load['data']:
            try:
                theme_id = get_theme_id_from_theme_name(theme_name=el['theme'])
                result = QuestionForDatabase(
                    theme_id=theme_id if theme_id else insert_data_with_theme_to_database(
                        data={'theme_name': el['theme']}
                    ),
                    question=el['question'],
                    explanation=el['explanation'],
                    correct_answer=el['correct_answer'],
                    incorrect_answers=[answer for answer in el['incorrect_answers'].values()],
                )
            except Exception as e:
                raise JsonIncorrectData(
                    'The data passed in the json file is incorrect, check the data against the documentation format.'
                    f'Info: {e}'
                )

            data.append(result)

    return data
