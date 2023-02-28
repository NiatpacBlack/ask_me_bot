"""This file describes the functionality of adding data from a json file to the database."""
from ask_me_bot.questions.exceptions import DataExportError, JsonKeysError
from models import postgres_client


test_data = (
    {
        "theme": "Python",
        "question": "Выберите неизменяемый тип данных",
        "explanation": "tuple - является неизменяемой структурой данных, элементы в нем нельзя изменить в программе, однако если элементом является изменяемая структура данных, то ее элементы по прежнему могут быть изменены.",
        "correct_answer": "tuple",
        "incorrect_answers": {
            "1": "list",
            "2": "byte arrays",
            "3": "dict"
        }
    },
    {
        "theme": "Python",
        "question": "Выберите изменяемый тип данных",
        "explanation": "dict - является изменяемым типом данных, его данные можно изменять по ходу действия программы",
        "correct_answer": "dict",
        "incorrect_answers": {
            "1": "float",
            "2": "tuple",
            "3": "frozenset",
            "4": "str"
        }
    },
    {
        "theme": "Python",
        "question": "Что делает функция isalnum ?",
        "explanation": "Эта функция возвращает истину, если все символы в строке являются алфавитно-цифровые и есть по крайней мере один символ, иначе ложь.",
        "correct_answer": "Вернет True, если в строке есть хотя бы один символ и все символы строки являются цифрами или буквами",
        "incorrect_answers": {
            "1": "Вернёт True , если в строке хотя бы одно число",
            "2": "Вернёт True , если в строке хотя бы одна буква",
            "3": "Вернёт False , если в строке хотя бы одна буква",
        }
    }
)


def parse_data_into_question_and_answer_format(data: tuple[dict[str, str | dict[str, str]], ...]) -> None:
    try:
        for dictionary in data:
            try:
                theme: str = dictionary["theme"]
                question: str = dictionary["question"]
                explanation: str = dictionary["explanation"]
                correct_answer: str = dictionary["correct_answer"]
                incorrect_answers: list[str, ...] = [answer for answer in dictionary["incorrect_answers"].values()]
            except KeyError:
                raise JsonKeysError("Invalid data received as input from json file.")

            theme_id = get_theme_id_from_theme_name(theme_name=theme)
            if not get_question_id_from_question_name(question_name=question):
                insert_question_in_questions_table(theme_id, question, explanation)
                insert_answers_for_question(
                    get_question_id_from_question_name(question_name=question),
                    correct_answer,
                    incorrect_answers,
                )
    except Exception as e:
        raise DataExportError(f"An unexpected error occurred while trying to export data to the database. Info: {e}")


def get_theme_id_from_theme_name(theme_name: str) -> int:
    query = f"""select theme_id from themes where theme_name = '{theme_name}';"""
    postgres_client.cursor.execute(query)
    theme_id = postgres_client.cursor.fetchone()[0]
    return theme_id


def insert_question_in_questions_table(theme_id: int, question: str, explanation: str) -> None:
    insert = f"""insert into questions (theme_id, question_name, explanation) values({theme_id}, '{question}', '{explanation}')"""
    postgres_client.cursor.execute(insert)
    postgres_client.db_connect.commit()


def get_question_id_from_question_name(question_name: str) -> int | bool:
    query = f"""select question_id from questions where question_name = '{question_name}';"""
    postgres_client.cursor.execute(query)
    result = postgres_client.cursor.fetchone()
    return result[0] if result else False


def insert_answers_for_question(question_id: int, correct_answer: str, incorrect_answers: list[str, ...]) -> None:
    answers = [correct_answer]
    answers.extend(incorrect_answers)
    for index, answer in enumerate(answers, 1):
        insert = f"""insert into answers (question_id, answer_name, is_right) values({question_id}, '{answer}', {"true" if index == 1 else "false"})"""
        postgres_client.cursor.execute(insert)
        postgres_client.db_connect.commit()


if __name__ == '__main__':
    parse_data_into_question_and_answer_format(test_data)
