from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, HiddenField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Optional
from app.models.user import User

class CSVUploadForm(FlaskForm):
    file = FileField('CSV File', validators=[
        FileRequired(),
        FileAllowed(['csv'], 'CSV files only!')
    ])

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class ProfileUpdateForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Update')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    club = StringField('Club', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        """
        This function validates whether a given `username` already exists or not
        by querying the database using `User.query.filter_by()` and checking if
        the result is not `None`.

        Args:
            username (str): The `username` input parameter passes the value of the
                `username` field of the current form data to the query performed
                on the `User` model.

        """
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        """
        This function checks if the provided email address is already associated
        with a user record on database and raises a ValidationError if it is found
        to be existing.

        Args:
            email (str): The `email` input parameter passes the value of the `email`
                field from the form to the function for validation.

        """
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')
        
class AddCourtForm(FlaskForm):
    court_name = StringField('Court Name', validators=[DataRequired()])
    submit = SubmitField('Add Court')

class EditCourtForm(FlaskForm):
    court_id = HiddenField('Court ID', validators=[DataRequired()])
    delete = SubmitField('Delete')
    edit = SubmitField('Edit')

class AddFlightForm(FlaskForm):
    flight_name = StringField('Flight Name', validators=[DataRequired()])
    submit = SubmitField('Add Flight')

class EditFlightForm(FlaskForm):
    flight_id = HiddenField('Flight ID', validators=[DataRequired()])
    delete = SubmitField('Delete')
    edit = SubmitField('Edit')

class EditClubAdminForm(FlaskForm):
    user_id = HiddenField('User ID', validators=[DataRequired()])
    toggle_authentication = SubmitField('Toggle', render_kw={'name': 'toggle_auth'})

class AddPlayerForm(FlaskForm):
    player_name = StringField('Player Name', validators=[DataRequired()])
    player_email = StringField('Player Email', validators=[DataRequired()]) # add email validation later
    submit = SubmitField('Add Player')

class EditPlayerForm(FlaskForm):
    player_id = HiddenField('Player ID', validators=[DataRequired()])
    delete = SubmitField('Delete')
    edit = SubmitField('Edit')