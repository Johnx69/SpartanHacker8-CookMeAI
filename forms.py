
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError, TextAreaField
from wtforms.validators import DataRequired, EqualTo, Length
from wtforms.widgets import TextArea
from flask_ckeditor import CKEditorField
from flask_wtf.file import FileField
# Create Login form
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField()

# Create a Post form
class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = CKEditorField('Content', validators=[DataRequired()], widget=TextArea())
    slug = StringField("Slug", validators=[DataRequired()], default='')
    submit = SubmitField('Submit')

class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    about_author = TextAreaField('About Author')
    password_hash = PasswordField("Password", validators=[DataRequired(), EqualTo(
        'password_hash2', message="Passwords Must Match")])
    password_hash2 = PasswordField("Confirm Password", validators=[DataRequired()])
    profile_pic = FileField()
    submit = SubmitField('Submit')

# Password Form
class PasswordForm(FlaskForm):
    email = StringField('What is your email', validators=[DataRequired()])
    password_hash = PasswordField(
        'What is your password', validators=[DataRequired()])
    submit = SubmitField("Submit")

# Create a search form
class SearchForm(FlaskForm):
    searched = StringField('Searched', validators=[DataRequired()])
    submit = SubmitField()

# Create a location form
class LocationForm(FlaskForm):
    location = StringField("Where are you guys? ", validators=[DataRequired()])
    submit = SubmitField('Submit')