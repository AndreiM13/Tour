import json
from datetime import date
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, RadioField, DateField, SelectField, IntegerField, HiddenField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
import re
from app.models import Admin, Tour,Departure
from flask import current_app

# Load countries with flags and prefixes
with open('countries.json', 'r', encoding='utf-8') as f:
    countries = json.load(f)

# Format country choices
country_prefix_choices = [
    (country['dial_code'], f"{country['flag']} {country['name']} ({country['dial_code']})")
    for country in countries
]

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=30)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        allowed_domain = 'allthings-socotra.com'
        domain_regex = r'^[a-zA-Z0-9_.+-]+@' + re.escape(allowed_domain) + r'$'
        if not re.match(domain_regex, email.data):
            raise ValidationError(f"Email must end with @{allowed_domain}")

        # Check for duplicates
        existing_admin = Admin.query.filter_by(email=email.data).first()
        if existing_admin:
            raise ValidationError('That email is already taken.')

    def validate_password(self, password):
        # Password strength check (e.g., require at least one digit, one letter, and one special character)
        if not re.search(r'[A-Za-z]', password.data):
            raise ValidationError('Password must contain at least one letter.')
        if not re.search(r'\d', password.data):
            raise ValidationError('Password must contain at least one number.')
        if not re.search(r'[\W_]', password.data):
            raise ValidationError('Password must contain at least one special character.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=30)])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

    def validate_email(self, email):
        allowed_domain = 'allthings-socotra.com'  # Replace with the domain you want to allow
        domain_regex = r'^[a-zA-Z0-9_.+-]+@' + re.escape(allowed_domain) + r'$'
        if not re.match(domain_regex, email.data):
            raise ValidationError(f"Email must end with @{allowed_domain}")


class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    message = TextAreaField('Message', validators=[DataRequired()])



class BookingForm(FlaskForm):
    client_name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=150)])
    client_email = StringField('Email Address', validators=[DataRequired(), Email()])
    country_code = SelectField('Country Prefix', choices=country_prefix_choices, validators=[DataRequired()])
    phone_number = StringField('Phone Number', validators=[DataRequired()])
    departure_id = HiddenField("Departure Date", validators=[DataRequired()])

    number_nights = RadioField(
        'Number of Nights',
        choices=[('4', '4 Nights'), ('7', '7 Nights'), ('10', '10 Nights')],
        validators=[DataRequired()]
    )
    number_people = IntegerField('Number of People', validators=[DataRequired()])
    tour_type = SelectField(
        'Tour Type',
        choices=[
            ('trekking', 'Trekking Tour'),
            ('full_island', 'Full Island Tour'),
            ('beach', 'Beach Lover'),
            ('vip', 'The VIP')
        ],
        validators=[DataRequired()]
    )


    submit = SubmitField('Book Tour')

    def validate_client_name(self, client_name):
        if not re.match(r'^[A-Za-z\s]+$', client_name.data):
            raise ValidationError('Name must contain only letters and spaces.')

    def validate_phone_number(self, phone_number):
        if not re.match(r'^\d{7,15}$', phone_number.data):
            raise ValidationError('Phone number must be between 7 and 15 digits and contain only numbers.')
        
    


class TourUpdateForm(FlaskForm):
    title = StringField('Tour Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    price = StringField('Price', validators=[DataRequired()])
    image_filename = StringField('Image Filename (URL)', validators=[DataRequired()])
    submit = SubmitField('Update Tour')



class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('New Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')

class ValidateAccountForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Resend Verification')