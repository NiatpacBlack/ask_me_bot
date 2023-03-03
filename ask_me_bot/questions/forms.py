from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length


class CreateQuestionForm(FlaskForm):
    theme = StringField(
        label='',
        description='Тема',
        render_kw={
            'class': 'form-control shadow'
        },
        validators=[DataRequired(), Length(max=50)],
    )
    question = TextAreaField(
        label='',
        description="Вопрос",
        render_kw={
            'class': 'form-control shadow'
        },
        validators=[DataRequired(), Length(max=255)],
    )
    explanation = StringField(
        label='',
        description="Объяснение ответа",
        render_kw={
            'class': 'form-control shadow'
        },
        validators=[DataRequired(), Length(max=200)],
    )
    correct_answer = StringField(
        label='',
        description="Правильный ответ",
        render_kw={
            'class': 'form-control shadow'
        },
        validators=[DataRequired(), Length(max=100)],
    )
    incorrect_answer1 = StringField(
        label='',
        description="1 Неправильный ответ",
        render_kw={
            'class': 'form-control shadow'
        },
        validators=[DataRequired(), Length(max=100)],
    )
    incorrect_answer2 = StringField(
        label='',
        description="2 Неправильный ответ",
        render_kw={
            'class': 'form-control shadow'
        },
        validators=[Length(max=100)],
    )
    incorrect_answer3 = StringField(
        label='',
        description="3 Неправильный ответ",
        render_kw={
            'class': 'form-control shadow'
        },
        validators=[Length(max=100)],
    )
    incorrect_answer4 = StringField(
        label='',
        description="4 Неправильный ответ",
        render_kw={
            'class': 'form-control shadow'
        },
        validators=[Length(max=100)],
    )
    incorrect_answer5 = StringField(
        label='',
        description="5 Неправильный ответ",
        render_kw={
            'class': 'form-control shadow'
        },
        validators=[Length(max=100)],
    )
    incorrect_answer6 = StringField(
        label='',
        description="6 Неправильный ответ",
        render_kw={
            'class': 'form-control shadow'
        },
        validators=[Length(max=100)],
    )
    incorrect_answer7 = StringField(
        label='',
        description="7 Неправильный ответ",
        render_kw={
            'class': 'form-control shadow'
        },
        validators=[Length(max=100)],
    )
    incorrect_answer8 = StringField(
        label='',
        description="8 Неправильный ответ",
        render_kw={
            'class': 'form-control shadow'
        },
        validators=[Length(max=100)],
    )
    incorrect_answer9 = StringField(
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
