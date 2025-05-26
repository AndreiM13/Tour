from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os
from dotenv import load_dotenv

# Initialize extensions
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()

# Initialize Flask app
app = Flask(__name__, static_folder='static')

# Load environment variables
load_dotenv()

# Configure app
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tours.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////data/tours.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions with the app
db.init_app(app)
bcrypt.init_app(app)
login_manager.init_app(app)

# Set the login view for Flask-Login
login_manager.login_view = "adminlogin"

# Import routes here to avoid circular import
# Import routes after app initialization
from app import routes
