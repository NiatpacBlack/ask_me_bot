from http import HTTPStatus

from flask import Flask
from flask import render_template, request

from ask_me_bot.config import FlaskConfig, EXPORT_PATH
from ask_me_bot.questions.converter import parse_data_from_json, add_data_to_json_file
from ask_me_bot.questions.forms import CreateQuestionForm
from ask_me_bot.questions.services import insert_data_with_questions_to_database, \
    get_all_questions_with_theme_name_from_db, get_question_with_theme_name, get_answers_for_question


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

        try:
            data = {
                "theme": request_data["theme"],
                "question": request_data["question"],
                "explanation": request_data["explanation"],
                "correct_answer": request_data["correct_answer"],
                "incorrect_answers": {key[-1]: value for key, value in request_data.items() if
                                      'incorrect_answer' in key and value}
            }
        except KeyError as e:
            return {
                "error": f"Invalid data passed in the request. Error information: {e}"
            }, HTTPStatus.BAD_REQUEST

        insert_data_with_questions_to_database([data])
        return {}, HTTPStatus.OK

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
        print(e)
        return {
            "error": f"The data has not been loaded into the database. Error information: {e}"
        }, HTTPStatus.INTERNAL_SERVER_ERROR
    return {}, HTTPStatus.OK


@app.route('/questions/')
def questions_view():
    """Displays a table with all questions from the database."""
    questions = get_all_questions_with_theme_name_from_db()
    return render_template(
        "questions_page.html",
        questions=questions,
    )


@app.route('/question/<question_id>/')
def question_view(question_id: str):
    """Displays full information about the question with question_id."""
    form = CreateQuestionForm()
    try:
        question_with_theme_name = get_question_with_theme_name(question_id)
        answers = get_answers_for_question(question_id)
    except Exception as e:
        print(e)
        return {
            "error": f"Failed to get question data with id {question_id}. Error information: {e}"
        }, HTTPStatus.INTERNAL_SERVER_ERROR

    form.theme.data = question_with_theme_name.theme_name
    form.question.data = question_with_theme_name.question_name
    form.explanation.data = question_with_theme_name.explanation
    form.correct_answer.data = answers.correct_answer
    for index, answer in enumerate(answers.incorrect_answers, 1):
        for el in form:
            if el.name == f'incorrect_answer{index}':
                el.data = answer

    return render_template(
        "question_detail_page.html",
        question=question_with_theme_name,
        form=form,
    )


if __name__ == '__main__':
    app.run()
