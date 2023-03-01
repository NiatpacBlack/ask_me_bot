from flask import Flask
from flask import render_template, request

from ask_me_bot.config import FlaskConfig
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
        data = request.form.to_dict()
        print(data)

    return render_template(
        "create_question_page.html",
        form=form,
    )


if __name__ == '__main__':
    app.run(debug=True)
