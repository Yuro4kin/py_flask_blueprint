from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Email, Length

# pip install email_validator
# В классе LoginForm() пропишем переменные которые будут представлять поля  email, password, checkbox, submit, ...
# -- переменная email ссылается на экземпляр класса StringField() - т.е. поле ввода обычное, с названием поля "Email" и параметром validators, который ссылается на список валидаторов для проверки корректности введенных данных
# чтоб мы могли использовать класс StringField() и валидатор Email мы должны их импортировать
# Базовый класс FlaskForm будем расширять с помощью дочернего класса LoginForm()
# Импортируем классы StringField, ... из модуля wtforms
# Импортируем валидаторы Email, ... из модуля wtforms.validators
# -- переменная psw ссылается на экземпляр класса PasswordField() - т.е. поле ввода обычное, с названием поля "Password" и параметром validators, DataRequired() - требует чтоб в поле был хотя бы 1 символ
class LoginForm(FlaskForm):
    email = StringField("Email: ", validators=[Email()])
    psw = PasswordField("Password: ", validators=[DataRequired(), Length(min=4, max=100)])
    remember = BooleanField("Запомнить", default=False)
    submit = SubmitField("Login")