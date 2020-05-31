from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Required
from bookreview.models import Person

class RegistrationForm(FlaskForm):
    username=StringField('Username', validators=[DataRequired(), Length(min=4,max=20)])
    email=StringField('Email',validators=[DataRequired(), Email()])
    password=PasswordField('Password',validators=[DataRequired()])
    confirmpassword=PasswordField('Confirm Password',validators=[DataRequired(), EqualTo('password')])
    submit=SubmitField('Sign Up')

    def validate_username(self, username):
        user=Person.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already exists. Try different Username.')

    def validate_email(self, email):
        email=Person.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('Email already exists. Try different Email.')

class LoginForm(FlaskForm):
    email=StringField('Email',validators=[DataRequired(), Email()])
    password=PasswordField('Password',validators=[DataRequired()])
    remember=BooleanField('Remember Me')
    submit=SubmitField('Sign In')

class ResetForm(FlaskForm):
    newpassword=PasswordField('Password',validators=[DataRequired()])
    confirmpassword=PasswordField('Confirm Password',validators=[DataRequired(), EqualTo('newpassword')])
    submit=SubmitField('Update')

class UpdateAccountForm(FlaskForm):
    username=StringField('Username', validators=[DataRequired(), Length(min=4,max=20)])
    email=StringField('Email',validators=[DataRequired(), Email()])
    submit=SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user=Person.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Username already exists. Try different Username.')

    def validate_email(self, email):
        if email.data != current_user.email:
            email=Person.query.filter_by(email=email.data).first()
            if email:
                raise ValidationError('Email already exists. Try different Email.')

    

class SearchForm(FlaskForm):
    choices=[('title', 'Title'),
               ('isbn', 'ISBN'),
               ('author', 'Author')]
    select = SelectField('Search', choices=choices)
    search = StringField('', validators=[DataRequired()])
