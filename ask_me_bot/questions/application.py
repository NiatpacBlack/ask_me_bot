from http import HTTPStatus

from flask import render_template, request
from flask.views import MethodView

from ask_me_bot.config import EXPORT_PATH
from ask_me_bot.questions.converter import parse_data_from_json
from ask_me_bot.questions.forms import CreateQuestionForm
from ask_me_bot.questions.services import insert_data_with_questions_to_database, \
    get_all_questions_with_theme_name_from_db, get_question_with_theme_name, get_answers_for_question, \
    parse_request_data_to_question_format, update_question_in_database


class CreateQuestionView(MethodView):
    """Page with a form for creating a question for a quiz."""

    def get(self):
        return render_template(
            "create_question_page.html",
            form=CreateQuestionForm(),
        )

    def post(self):
        try:
            data = parse_request_data_to_question_format(request.form.to_dict())
        except KeyError as e:
            return {
                "error": f"Invalid data passed in the request. Error information: {e}"
            }, HTTPStatus.BAD_REQUEST

        insert_data_with_questions_to_database([data])
        return {}, HTTPStatus.OK


class PushJsonToDbView(MethodView):
    """Writes data from json file to database."""

    def get(self):
        try:
            data = parse_data_from_json(path_to_file=EXPORT_PATH)
            insert_data_with_questions_to_database(data)
        except Exception as e:
            print(e)
            return {
                "error": f"The data has not been loaded into the database. Error information: {e}"
            }, HTTPStatus.INTERNAL_SERVER_ERROR
        return {}, HTTPStatus.OK


class QuestionsView(MethodView):
    """Displays a table with all questions from the database."""

    def get(self):
        questions = get_all_questions_with_theme_name_from_db()
        return render_template(
            "questions_page.html",
            questions=questions,
        )


class QuestionView(MethodView):
    """Displays full information about the question with question_id."""

    def get(self, question_id: str):
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
        form.correct_answer.data = answers.correct_answer.answer_name
        for index, answer in enumerate(answers.incorrect_answers, 1):
            for el in form:
                if el.name == f'incorrect_answer{index}':
                    el.data = answer.answer_name
        return render_template(
            "question_detail_page.html",
            question=question_with_theme_name,
            correct_answer_id=str(answers.correct_answer.answer_id),
            incorrect_answers_id=" ".join([str(answer.answer_id) for answer in answers.incorrect_answers]),
            form=form,
        )

    def put(self, question_id: str):
        form = CreateQuestionForm()
        if form.validate_on_submit():
            request_data = request.form.to_dict()
            try:
                data = parse_request_data_to_question_format(request_data)
                incorrect_answers_id = request_data["incorrect_answers_id"].split()
                correct_answer_id = request_data["correct_answers_id"]
            except KeyError as e:
                return {
                    "error": f"Invalid data passed in the request. Error information: {e}"
                }, HTTPStatus.BAD_REQUEST
            update_question_in_database(data, question_id, correct_answer_id, incorrect_answers_id)
            return {}, HTTPStatus.OK
