from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, NumberRange

class RegisterForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired(), Length(3, 50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(6)])
    confirm = PasswordField('Повторите пароль', validators=[DataRequired(), EqualTo('password', message='Пароли должны совпадать')])
    submit = SubmitField('Зарегистрироваться')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')

class ReviewForm(FlaskForm):
    rating = IntegerField('Оценка (1–5)', validators=[DataRequired(), NumberRange(1, 5)])
    text = TextAreaField('Ваш отзыв', validators=[DataRequired(), Length(10, 500)])
    submit = SubmitField('Отправить отзыв')