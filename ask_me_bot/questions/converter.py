"""This file describes the functionality of parsing and adding data to json file."""
import json

from ask_me_bot.config import EXPORT_PATH


def add_data_to_json_file(new_data: dict[str, str, str, str, dict[str, str]]) -> None:
    """Appends the passed data to the json file."""
    with open(EXPORT_PATH, mode='r+', encoding='utf-8') as file:
        data = json.load(file)
        if data.get('data', False):
            data["data"].append(new_data)
        else:
            data["data"] = {}
        json.dump(data, file)


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
