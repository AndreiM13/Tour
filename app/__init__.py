from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.extensions import db, bcrypt, login_manager, mail  # ✅ import from extensions
import os
from dotenv import load_dotenv



# Initialize Flask app
app = Flask(__name__, static_folder='static')

# Load environment variables
load_dotenv()

# Configure app
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tours.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////new_data/tours.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# Email settings
app.config['MAIL_SERVER'] = 'mail.privateemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False   # Use True if you switch to port 465
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')  # e.g. your full email address
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_USERNAME')

# Initialize extensions with the app
db.init_app(app)
bcrypt.init_app(app)
login_manager.init_app(app)
mail.init_app(app)  # <-- add this line

# Set the login view for Flask-Login
login_manager.login_view = "adminlogin"

# Import routes here to avoid circular import
# Import routes after app initialization
from app import routes
