from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length

from ask_me_bot.questions.services import get_themes_for_choices


class CreateThemeForm(FlaskForm):
    theme_name = StringField(
        label='',
        description='Тема',
        render_kw={
            'class': 'form-control shadow'
        },
        validators=[DataRequired(), Length(max=100)],
    )
    submit = SubmitField(
        "Добавить тему",
        render_kw={
            'class': 'btn-lg btn-success mt-2',
            'form': 'addThemeForm',
        },
    )


class CreateQuestionForm(FlaskForm):
    theme = SelectField(
        label='',
        description='Тема',
        render_kw={
            'class': 'form-select shadow'
        },
        validators=[DataRequired()],
        choices=get_themes_for_choices(),
    )
    question = TextAreaField(
        label='',
        description="Вопрос",
        render_kw={
            'class': 'form-control shadow'
        },
        validators=[DataRequired(), Length(max=255)],
    )
    explanation = TextAreaField(
        label='',
        description="Объяснение ответа",
        render_kw={
            'class': 'form-control shadow'
        },
        validators=[DataRequired(), Length(max=200)],
    )
    correct_answer = TextAreaField(
        label='',
        description="Правильный ответ",
        render_kw={
            'class': 'form-control shadow'
        },
        validators=[DataRequired(), Length(max=100)],
    )
    incorrect_answer1 = TextAreaField(
        label='',
        description="1 Неправильный ответ",
        render_kw={
            'class': 'form-control shadow'
        },
        validators=[DataRequired(), Length(max=100)],
    )
    incorrect_answer2 = TextAreaField(
        label='',
        description="2 Неправильный ответ",
        render_kw={
            'class': 'form-control shadow'
        },
        validators=[Length(max=100)],
    )
    incorrect_answer3 = TextAreaField(
        label='',
        description="3 Неправильный ответ",
        render_kw={
            'class': 'form-control shadow'
        },
        validators=[Length(max=100)],
    )
    incorrect_answer4 = TextAreaField(
        label='',
        description="4 Неправильный ответ",
        render_kw={
            'class': 'form-control shadow'
        },
        validators=[Length(max=100)],
    )
    incorrect_answer5 = TextAreaField(
        label='',
        description="5 Неправильный ответ",
        render_kw={
            'class': 'form-control shadow'
        },
        validators=[Length(max=100)],
    )
    incorrect_answer6 = TextAreaField(
        label='',
        description="6 Неправильный ответ",
        render_kw={
            'class': 'form-control shadow'
        },
        validators=[Length(max=100)],
    )
    incorrect_answer7 = TextAreaField(
        label='',
        description="7 Неправильный ответ",
        render_kw={
            'class': 'form-control shadow'
        },
        validators=[Length(max=100)],
    )
    incorrect_answer8 = TextAreaField(
        label='',
        description="8 Неправильный ответ",
        render_kw={
            'class': 'form-control shadow'
        },
        validators=[Length(max=100)],
    )
    incorrect_answer9 = TextAreaField(
        label='',
        description="9 Неправильный ответ",
        render_kw={
            'class': 'form-control shadow'
        },
        validators=[Length(max=100)],
    )
    submit = SubmitField(
        "Добавить вопрос",
        render_kw={
            'class': 'btn-lg btn-success',
            'form': 'addQuestionForm',
        },
    )
