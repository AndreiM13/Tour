import json
import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, RadioField, DateField, SelectField
from wtforms.validators import DataRequired, Length, Email,EqualTo, ValidationError
import re
from app.models import Admin, Tour

class RegistrationForm(FlaskForm):

    email = StringField('Email',
                        validators=[DataRequired(),Email()])
    password = PasswordField('Password',
                             validators=[DataRequired(), Length(min=6, max=30)])
    confirm_password = PasswordField('Cofirm Password',
                             validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        allowed_domain = 'blog.com'
        domain_regex = r'^[a-zA-Z0-9_.+-]+@' + re.escape(allowed_domain) + r'$'
        if not re.match(domain_regex, email.data):
            raise ValidationError(f"Email must end with @{allowed_domain}")

        # Check for duplicates
        existing_admin = Admin.query.filter_by(email=email.data).first()
        if existing_admin:
            raise ValidationError('That email is already taken.')



    
class LoginForm(FlaskForm):

    email = StringField('Email',
                        validators=[DataRequired(),Email()])
    password = PasswordField('Password',
                             validators=[DataRequired(), Length(min=6, max=30)])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

    # Custom validator to check if email ends with a specific domain using regular expression
    def validate_email(self, email):
        allowed_domain = 'blog.com'  # Replace with the domain you want to allow
        domain_regex = r'^[a-zA-Z0-9_.+-]+@' + re.escape(allowed_domain) + r'$'
        if not re.match(domain_regex, email.data):
            raise ValidationError(f"Email must end with @{allowed_domain}")
        
class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    message = TextAreaField('Message', validators=[DataRequired()])

# Load countries with flags and prefixes
with open('countries.json', 'r', encoding='utf-8') as f:
    countries = json.load(f)

# Format country choices
country_prefix_choices = [
    (country['dial_code'], f"{country['flag']} {country['name']} ({country['dial_code']})")
    for country in countries
]


class BookingForm(FlaskForm):
    client_name = StringField('Full Name', validators=[DataRequired()])
    client_email = StringField('Email Address', validators=[DataRequired(), Email()])
    country_code = SelectField('Country Prefix', choices=country_prefix_choices, validators=[DataRequired()])
    phone_number = StringField('Phone Number', validators=[DataRequired()])
    travel_date = DateField(
        'Travel Date',
        validators=[DataRequired()],
        format='%Y-%m-%d',
        default=datetime.date.today
    )
    number_nights = RadioField(
        'Number of Nights',
        choices=[('6', '6 Nights'), ('8', '8 Nights'), ('11', '11 Nights')],
        validators=[DataRequired()]
    )
    number_people = StringField('Number of People', validators=[DataRequired()])
    tour_type = SelectField(
        'Tour Type',
        choices=[('photographer', 'The Photographer'),
                 ('explorer', 'The Explorer'),
                 ('beach', 'The Beach Potato'),
                 ('vip', 'The VIP')],
        validators=[DataRequired()]
    )
    tour_id = SelectField('Tour', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Book Tour')

