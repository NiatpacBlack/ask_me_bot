from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length


class CreateQuestionForm(FlaskForm):
    theme = StringField(
        'Тема',
        render_kw={
            'class': 'form-control'
        },
        validators=[DataRequired(), Length(max=50)],
    )
    question = TextAreaField(
        "Вопрос",
        render_kw={
            'class': 'form-control'
        },
        validators=[DataRequired(), Length(max=255)],
    )
    explanation = StringField(
        "Объяснение ответа",
        render_kw={
            'class': 'form-control'
        },
        validators=[DataRequired(), Length(max=200)],
    )
    correct_answer = StringField(
        "Правильный ответ",
        render_kw={
            'class': 'form-control'
        },
        validators=[DataRequired(), Length(max=100)],
    )
    incorrect_answer1 = StringField(
        "1 Неправильный ответ",
        render_kw={
            'class': 'form-control'
        },
        validators=[DataRequired(), Length(max=100)],
    )
    incorrect_answer2 = StringField(
        "2 Неправильный ответ",
        render_kw={
            'class': 'form-control'
        },
        validators=[Length(max=100)],
    )
    incorrect_answer3 = StringField(
        "3 Неправильный ответ",
        render_kw={
            'class': 'form-control'
        },
        validators=[Length(max=100)],
    )
    incorrect_answer4 = StringField(
        "4 Неправильный ответ",
        render_kw={
            'class': 'form-control'
        },
        validators=[Length(max=100)],
    )
    incorrect_answer5 = StringField(
        "5 Неправильный ответ",
        render_kw={
            'class': 'form-control'
        },
        validators=[Length(max=100)],
    )
    incorrect_answer6 = StringField(
        "6 Неправильный ответ",
        render_kw={
            'class': 'form-control'
        },
        validators=[Length(max=100)],
    )
    incorrect_answer7 = StringField(
        "7 Неправильный ответ",
        render_kw={
            'class': 'form-control'
        },
        validators=[Length(max=100)],
    )
    incorrect_answer8 = StringField(
        "8 Неправильный ответ",
        render_kw={
            'class': 'form-control'
        },
        validators=[Length(max=100)],
    )
    incorrect_answer9 = StringField(
        "9 Неправильный ответ",
        render_kw={
            'class': 'form-control'
        },
        validators=[Length(max=100)],
    )
    submit = SubmitField(
        "Добавить вопрос",
        render_kw={
            'class': 'btn btn-success',
            'form': 'addQuestionForm',
        },
    )
