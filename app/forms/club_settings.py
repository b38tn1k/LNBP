from wtforms import validators, StringField, PasswordField, HiddenField, IntegerField, FormField, SelectField
from app.forms import BaseForm

class ClubSetup(BaseForm):
    name = StringField('Club Name', validators=[validators.Optional()])  # Optional field
    email = StringField('Contact Email', validators=[validators.Optional(), validators.Email()])  # Email is optional, but if provided, it should be valid.
    contact_number = StringField('Contact Number', validators=[validators.Optional(), validators.Length(max=50)])  # Optional field with a max length of 50 characters
    street_address = StringField('Street Address', validators=[validators.Optional()])  # Optional field
    street_address2 = StringField('', validators=[validators.Optional()])  # Optional field
    city = StringField('City', validators=[validators.Optional(), validators.Length(max=100)])  # Optional field with a max length of 100 characters
    state = StringField('State', validators=[validators.Optional(), validators.Length(max=100)])  # Optional field with a max length of 100 characters
    zip_code = StringField('ZIP Code', validators=[validators.Optional(), validators.Length(max=15)])  # Optional field with a max length of 15 characters
    country = StringField('Country', validators=[validators.Optional(), validators.Length(max=100)])  # Optional field with a max length of 100 characters

class FacilitySetup(BaseForm):
    name = StringField('Facility Name', validators=[validators.InputRequired()])
    facility_type = SelectField('Facility Type', choices=[('1', 'Tennis Court'), ('2', 'Pickle Ball Court'), ('3', 'Gladiator Pit')])