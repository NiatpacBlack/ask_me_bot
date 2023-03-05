import os
from dotenv import load_dotenv


load_dotenv()

# Variable in which the executable directory of the script is placed
_basedir = os.path.abspath(os.path.dirname(__file__))

# Telegram bot token
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Data to connect to PostgresQL database
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

# Default path for json file with questions
EXPORT_PATH = 'export/questions.json'

# Default time zone
TIME_ZONE = "Europe/Minsk"

# Folder for html files
TEMPLATES_DIR = os.path.join(_basedir, "questions/templates")

# Folder for static files
STATIC_DIR = os.path.join(_basedir, "questions/static")


class FlaskConfig:
    """Description of all Flask-application configuration settings."""

    # Debug Mode
    DEBUG = True
    # The secret key is set either in an environment variable or directly.
    SECRET_KEY = os.getenv("FLASK_SECRET_KEY") or "any_key"
