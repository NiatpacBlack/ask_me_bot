"""This file describes all the url paths of the admin panel."""
from flask.blueprints import Blueprint

from ask_me_bot.questions.views import (
    MainView,
    QuestionView,
    CreateQuestionView,
    CreateThemeView,
    ImportDataToDbView,
    ThemeView,
    ExportDataFromDbView,
)


questions_routes = Blueprint(name="questions", import_name=__name__)

questions_routes.add_url_rule("/", view_func=MainView.as_view("main"))

questions_routes.add_url_rule(
    "/question/create/", view_func=CreateQuestionView.as_view("create_question")
)
questions_routes.add_url_rule(
    "/question/<int:question_id>/", view_func=QuestionView.as_view("question")
)

questions_routes.add_url_rule(
    "/theme/create/", view_func=CreateThemeView.as_view("create_theme")
)
questions_routes.add_url_rule(
    "/theme/<int:theme_id>/", view_func=ThemeView.as_view("theme")
)
questions_routes.add_url_rule(
    "/import/", view_func=ImportDataToDbView.as_view("import")
)
questions_routes.add_url_rule(
    "/export/", view_func=ExportDataFromDbView.as_view("export")
)
