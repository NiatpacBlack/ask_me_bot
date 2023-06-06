"""This file contains all the view functions for the admin panel."""
import traceback
from http import HTTPStatus

from flask import render_template, request
from flask.views import MethodView

from ask_me_bot.config import IMPORT_PATH, logger, IMPORT_FILE_NAME
from ask_me_bot.questions.converter import parse_data_from_json, add_data_to_json_file
from ask_me_bot.questions.forms import CreateQuestionForm, CreateThemeForm
from ask_me_bot.questions.services import (
    insert_data_with_questions_to_database,
    get_all_questions_with_theme_name_from_db,
    get_question_with_theme_name,
    get_answers_for_question,
    parse_request_data_to_question_format,
    update_question_in_database,
    delete_question_from_database,
    parse_request_data_to_theme_format,
    insert_data_with_theme_to_database,
    get_all_themes_from_db,
    get_themes_for_choices,
    get_theme_from_db,
    update_theme_in_database,
    delete_theme_from_database,
    get_question_data_from_database,
    parse_questions_data_to_json,
)


class ImportDataToDbView(MethodView):
    """Writes data from json file to database."""

    def get(self):
        try:
            data = parse_data_from_json(
                path_to_file=IMPORT_PATH, file_name=IMPORT_FILE_NAME
            )
            insert_data_with_questions_to_database(data)
        except Exception as e:
            logger.exception(Exception)
            logger.error(traceback.format_exc())
            return {
                "error": f"The data has not been loaded into the database. Error information: {e}"
            }, HTTPStatus.INTERNAL_SERVER_ERROR
        return {}, HTTPStatus.OK


class ExportDataFromDbView(MethodView):
    """Export data from database to json file."""

    def get(self):
        try:
            questions_data = get_question_data_from_database()
            questions_json_data = parse_questions_data_to_json(questions_data)
            add_data_to_json_file(questions_json_data)
        except Exception as e:
            logger.exception(Exception)
            logger.error(traceback.format_exc())
            return {
                "error": f"The data has not been loaded into a json file. Error information: {e}"
            }, HTTPStatus.INTERNAL_SERVER_ERROR
        return {}, HTTPStatus.OK


class MainView(MethodView):
    """Displays a table with all questions and table with all themes from the database."""

    def get(self):
        questions = get_all_questions_with_theme_name_from_db()
        themes = get_all_themes_from_db()
        return render_template(
            "main_page.html",
            questions=questions,
            themes=themes,
        )


class QuestionView(MethodView):
    """Displays full information about the question with question_id."""

    def get(self, question_id: str):
        form = CreateQuestionForm()

        try:
            question_with_theme_name = get_question_with_theme_name(question_id)
            answers = get_answers_for_question(question_id)

            # Adding theme, question, and answers data to a form
            form.theme_id.data = question_with_theme_name.theme_name
            form.theme_id.choices = sorted(
                get_themes_for_choices(),
                key=lambda choice: choice != (question_with_theme_name.theme_id, question_with_theme_name.theme_name),
            )
            form.question.data = question_with_theme_name.question_name
            form.explanation.data = question_with_theme_name.explanation
            form.detail_explanation.data = question_with_theme_name.detail_explanation
            form.correct_answer.data = answers.correct_answer.answer_name
            for index, answer in enumerate(answers.incorrect_answers, 1):
                for field in form:
                    if field.name == f"incorrect_answer{index}":
                        field.data = answer.answer_name

        except Exception as e:
            logger.exception(Exception)
            logger.error(traceback.format_exc())
            return {
                "error": f"Failed to get question data with id {question_id}. Error information: {e}"
            }, HTTPStatus.INTERNAL_SERVER_ERROR

        return render_template(
            "question_detail_page.html",
            question=question_with_theme_name,
            correct_answer_id=str(answers.correct_answer.answer_id),
            incorrect_answers_id=" ".join(
                [str(answer.answer_id) for answer in answers.incorrect_answers]
            ),
            form=form,
        )

    def put(self, question_id: str):
        request_data = request.form.to_dict()

        try:
            data = parse_request_data_to_question_format(request_data)
            incorrect_answers_id = request_data["incorrect_answers_id"].split()
            correct_answer_id = request_data["correct_answers_id"]
        except KeyError as e:
            logger.exception(KeyError)
            logger.error(traceback.format_exc())
            return {
                "error": f"Invalid data passed in the request. Error information: {e}"
            }, HTTPStatus.BAD_REQUEST

        update_question_in_database(
            data, question_id, correct_answer_id, incorrect_answers_id
        )
        return {}, HTTPStatus.OK

    def delete(self, question_id: str):
        try:
            delete_question_from_database(question_id)
        except Exception as e:
            logger.exception(Exception)
            logger.error(traceback.format_exc())
            return {
                "error": f"Failed to delete question number {question_id}. Error information: {e}"
            }, HTTPStatus.INTERNAL_SERVER_ERROR
        return {}, HTTPStatus.OK


class CreateQuestionView(MethodView):
    """Page with a form for creating a question for a quiz."""

    def get(self):
        form = CreateQuestionForm()
        form.theme_id.choices = get_themes_for_choices()

        return render_template(
            "create_question_page.html",
            form=form,
        )

    def post(self):
        try:
            data = parse_request_data_to_question_format(request.form.to_dict())
        except KeyError as e:
            logger.exception(KeyError)
            logger.error(traceback.format_exc())
            return {
                "error": f"Invalid data passed in the request. Error information: {e}"
            }, HTTPStatus.BAD_REQUEST

        insert_data_with_questions_to_database([data])
        return {}, HTTPStatus.OK


class ThemeView(MethodView):
    def get(self, theme_id: str):
        form = CreateThemeForm()

        try:
            theme = get_theme_from_db(theme_id)

            # Adding theme data to a form
            form.theme_name.data = theme.theme_name

        except Exception as e:
            logger.exception(Exception)
            logger.error(traceback.format_exc())
            return {
                "error": f"Failed to get theme data with id {theme_id}. Error information: {e}"
            }, HTTPStatus.INTERNAL_SERVER_ERROR

        return render_template(
            "theme_detail_page.html",
            theme=theme,
            form=form,
        )

    def put(self, theme_id: str):

        request_data = request.form.to_dict()

        try:
            data = parse_request_data_to_theme_format(request_data)
        except KeyError as e:
            logger.exception(KeyError)
            logger.error(traceback.format_exc())
            return {
                "error": f"Invalid data passed in the request. Error information: {e}"
            }, HTTPStatus.BAD_REQUEST

        update_theme_in_database(data, theme_id)
        return {}, HTTPStatus.OK

    def delete(self, theme_id: str):
        try:
            delete_theme_from_database(theme_id)
        except Exception as e:
            logger.exception(Exception)
            logger.error(traceback.format_exc())
            return {
                "error": f"Failed to delete theme number {theme_id}. Error information: {e}"
            }, HTTPStatus.INTERNAL_SERVER_ERROR
        return {}, HTTPStatus.OK


class CreateThemeView(MethodView):
    def get(self):
        return render_template(
            "create_theme_page.html",
            form=CreateThemeForm(),
        )

    def post(self):
        try:
            data = parse_request_data_to_theme_format(request.form.to_dict())
        except KeyError as e:
            logger.exception(KeyError)
            logger.error(traceback.format_exc())
            return {
                "error": f"Invalid data passed in the request. Error information: {e}"
            }, HTTPStatus.BAD_REQUEST

        insert_data_with_theme_to_database(data)
        return {}, HTTPStatus.OK
