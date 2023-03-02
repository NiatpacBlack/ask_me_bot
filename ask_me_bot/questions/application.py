import json

from flask import Flask
from flask import render_template, request

from ask_me_bot.config import FlaskConfig, EXPORT_PATH
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


if __name__ == '__main__':
    app.run(debug=True)
