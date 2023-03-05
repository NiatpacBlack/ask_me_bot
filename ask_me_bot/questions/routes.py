from flask.blueprints import Blueprint

from ask_me_bot.questions.application import CreateQuestionView, PushJsonToDbView, QuestionsView, QuestionView


questions_routes = Blueprint(name="questions", import_name=__name__)

questions_routes.add_url_rule('/', view_func=CreateQuestionView.as_view('create_question'))
questions_routes.add_url_rule('/push/', view_func=PushJsonToDbView.as_view('push_json'))
questions_routes.add_url_rule('/questions/', view_func=QuestionsView.as_view('questions'))
questions_routes.add_url_rule('/question/<question_id>/', view_func=QuestionView.as_view('question'))
