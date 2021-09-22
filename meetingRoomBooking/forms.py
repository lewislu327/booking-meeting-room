from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.fields.html5 import DateField, TimeField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from meetingRoomBooking.models import User


class RegistrationForm(FlaskForm):
    username = StringField('User Name', validators=[
                           DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField(
        'Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                'That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(
                'That email is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class PostForm(FlaskForm):
    date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()])
    roomName = SelectField('Room',  choices=[(
        '大會議室', '大會議室'), ('中會議室', '中會議室'), ('小會議室', '小會議室')], validators=[DataRequired()])
    start_at = SelectField('Start at', choices=[(
        '08:00'), ('09:00'), ('10:00'), ('11:00'), ('12:00'), ('13:00'),('14:00'), ('15:00'), ('16:00'),('17:00'), ('18:00')],validators=[DataRequired()])
    end_at = SelectField('End at', choices=[(
        '08:00'), ('09:00'), ('10:00'), ('11:00'), ('12:00'), ('13:00'), ('14:00'), ('15:00'), ('16:00'), ('17:00'), ('18:00')], validators=[DataRequired()])
    submit = SubmitField('')
