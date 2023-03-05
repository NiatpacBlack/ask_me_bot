from flask import Flask

from ask_me_bot.config import FlaskConfig, TEMPLATES_DIR, STATIC_DIR
from ask_me_bot.questions.routes import questions_routes


app = Flask(__name__, template_folder=TEMPLATES_DIR, static_folder=STATIC_DIR)
app.config.from_object(FlaskConfig)
app.register_blueprint(questions_routes)
