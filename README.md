## Telegram bot - Ask Me About Programming Bot

This Telegram bot is designed to simplify the learning of programming languages, new technologies, or any other theoretical knowledge that needs to be reviewed from time to time.

The Telegram bot can send you quiz questions that you must answer correctly. It will also provide information with an explanation of the answer.

In case you do not want to choose an answer from multiple options, you can select a simple question that you can answer on your own and compare the answer with the correct option.

For convenient addition and editing of questions, the application has a web interface written in Flask, which is a kind of admin panel.

Through it, you can add a new topic for questions, add and edit questions, delete questions, and also view questions in the form of a table that can be sorted to find the needed question.

## Launch of the project

* ![Python Version](https://img.shields.io/badge/python-3.11-green) ![Code Style](https://img.shields.io/badge/code%20style-black-blue)
* PostgreSQL 15.1 database
* Install dependencies from requirements.txt: `pip install -r requirements.txt`
* To connect to the database, add to the environment variables in the .env.example file, **rename the file to .env**:
  - `DB_NAME` (name of your PostgreSQL database)
  - `DB_USER` (your PostgreSQL username)
  - `DB_PASSWORD` (password of your PostgreSQL user)
  - `DB_HOST` (your PostgreSQL database host)
  - `DB_PORT` (port of your PostgreSQL database)
