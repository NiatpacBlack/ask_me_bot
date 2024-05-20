"""This file stores all project settings and static variables."""
import os
from dotenv import load_dotenv
from loguru import logger


load_dotenv()

# Variable in which the executable directory of the script is placed
_basedir = os.path.abspath(os.path.dirname(__file__))

# Log file settings
logger.add(
    os.path.join(_basedir, "logs/logs.log"),
    format="{time} {level} {message}",
    level="DEBUG",
    rotation="1 day",
    compression="zip",
)

# Telegram bot token
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Data to connect to PostgresQL database
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

# Default path for json file with questions
EXPORT_PATH = "ask_me_bot/questions/export/"
IMPORT_PATH = "ask_me_bot/questions/import/"
IMPORT_FILE_NAME = os.getenv("IMPORT_FILE_NAME")

# Default time zone
TIME_ZONE = "Europe/Minsk"

# Folder for html files
TEMPLATES_DIR = os.path.join(_basedir, "questions/templates")

# Folder for static files
STATIC_DIR = os.path.join(_basedir, "questions/static")

# A timer that determines the number of seconds it takes to answer a blitz question
BLITZ_TIMER = 30


class FlaskConfig:
    """Description of all Flask-application configuration settings."""

    # Debug Mode
    DEBUG = True
    # The secret key is set either in an environment variable or directly.
    SECRET_KEY = os.getenv("FLASK_SECRET_KEY") or "any_key"


# The name of groups that store topics for a certain type of question in the telegram bot
JUST_QUESTION_GROUP_NAME = "Just Question"

# Topics listed in this variable will be excluded from the output in the bot
EXCLUDED_QUESTION_TOPICS = ["Python Quiz", ]
