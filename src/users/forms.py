from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from src.models import User

class RegistrationForm(FlaskForm):
    username = StringField("Username", validators = [DataRequired(), Length(min = 4, max = 25)])
    email = StringField("Email", validators = [DataRequired(), Email()])
    phone = StringField("Phone", validators = [DataRequired()])
    password = PasswordField("Password", validators = [DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators = [DataRequired(), EqualTo("password")])
    submit = SubmitField("Sign Up")
    reset = SubmitField("Reset")
    
    def validate_username(self, username):
        user = User.query.filter_by(username = username.data).first()
        if user:
            raise ValidationError("The username has been registered before. Please use another one.")

    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()
        if user:
            raise ValidationError("The email has been registered before. Please use another one.")

    def validate_phone(self, phone):
        user = User.query.filter_by(phone = phone.data).first()
        if user:
            raise ValidationError("The phone has been registered before. Please use another one.")

class LoginForm(FlaskForm):
    # username = StringField("Username", validators = [DataRequired(), Length(min = 4, max = 25)])
    email = StringField("Email", validators = [DataRequired(), Email()])
    password = PasswordField("Password", validators = [DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")

class UpdateAccountForm(FlaskForm):
    username = StringField("Username", validators = [DataRequired(), Length(min = 4, max = 25)])
    email = StringField("Email", validators = [DataRequired(), Email()])
    phone = StringField("Phone", validators = [DataRequired()])
    submit = SubmitField("Update")
    
    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username = username.data).first()
            if user:
                raise ValidationError("The username has been registered before. Please use another one.")

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email = email.data).first()
            if user:
                raise ValidationError("The email has been registered before. Please use another one.")

    def validate_phone(self, phone):
        if phone.data != current_user.phone:
            user = User.query.filter_by(phone = phone.data).first()
            if user:
                raise ValidationError("The phone has been registered before. Please use another one.")

class RequestResetForm(FlaskForm):
    email = StringField("Email", validators = [DataRequired(), Email()])
    submit = SubmitField("Request Password Reset")

    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()
        if user is None:
            raise ValidationError("There is no account with that email. You must register first.")

class ResetPasswordForm(FlaskForm):
    password = PasswordField("Password", validators = [DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators = [DataRequired(), EqualTo("password")])
    submit = SubmitField("Reset Password")