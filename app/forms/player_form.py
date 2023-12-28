from app.forms import BaseForm
from wtforms import StringField, BooleanField, IntegerField, SelectField
from wtforms.validators import DataRequired, Email, Optional

class PlayerForm(BaseForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[Email()])
    contact_number = StringField('Contact Number', validators=[Optional()])
    communication_preference_mobile = BooleanField('Mobile Communication OK')
    communication_preference_email = BooleanField('Email Communication OK')
    gender = SelectField('Gender', choices=[('unknown', 'Unknown'), ('male', 'Male'), ('female', 'Female'), ('other', 'Other')], validators=[Optional()])
    club_ranking = IntegerField('Club Ranking', validators=[Optional()])