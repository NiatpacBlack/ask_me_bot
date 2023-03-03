import json
from http import HTTPStatus

from flask import Flask
from flask import render_template, request

from ask_me_bot.config import FlaskConfig, EXPORT_PATH
from ask_me_bot.questions.converter import parse_data_from_json, insert_data_with_questions_to_database
from ask_me_bot.questions.forms import CreateQuestionForm


def create_app():
    application = Flask(__name__)
    application.config.from_object(FlaskConfig)

    return application


app = create_app()


@app.route('/', methods=["GET", "POST"])
def create_question_view():
    """Page with a form for creating a question for a quiz."""

    form = CreateQuestionForm()

    if request.method == "POST":
        request_data = request.form.to_dict()
        del request_data['csrf_token']

        new_data = {
            "theme": request_data["theme"],
            "question": request_data["question"],
            "explanation": request_data["explanation"],
            "correct_answer": request_data["correct_answer"],
            "incorrect_answers": {key[-1]: value for key, value in request_data.items() if
                                  'incorrect_answer' in key and value}
        }
        with open(EXPORT_PATH) as f:
            data = json.load(f)

        data["data"].append(new_data)

        with open(EXPORT_PATH, 'w') as f:
            json.dump(data, f)

    return render_template(
        "create_question_page.html",
        form=form,
    )


@app.route('/push/')
def push_json_to_database():
    """Writes data from json file to database."""
    try:
        data = parse_data_from_json(path_to_file=EXPORT_PATH)
        insert_data_with_questions_to_database(data)
    except Exception as e:
        return {
            "error": f"The data has not been loaded into the database. Error information: {e}"
        }, HTTPStatus.INTERNAL_SERVER_ERROR
    return {}, HTTPStatus.OK


if __name__ == '__main__':
    app.run(debug=True)
