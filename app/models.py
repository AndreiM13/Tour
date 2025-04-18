from datetime import datetime
from app import db
from flask_login import UserMixin

# Import login_manager from the app package
from app import login_manager

@login_manager.user_loader  # Use the login_manager correctly here
def load_user(user_id):
    return Admin.query.get(int(user_id))

class Admin(db.Model, UserMixin):
    __tablename__ = 'admins'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    gallery_posts = db.relationship('Gallery', backref='admin', lazy=True)
    tours = db.relationship('Tour', backref='admin', lazy=True)

class Gallery(db.Model):
    __tablename__ = 'gallery'
    id = db.Column(db.Integer, primary_key=True)
    image_filename = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    alt_text = db.Column(db.String(255), nullable=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('admins.id'), nullable=False)
class Tour(db.Model):
    __tablename__ = 'tours'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    number_person = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    admin_id = db.Column(db.Integer, db.ForeignKey('admins.id'), nullable=False)

    # Relationship to Booking without backref to avoid conflict with 'tour_id'
    bookings = db.relationship('Booking', backref='tour', lazy=True)


class Booking(db.Model):
    __tablename__ = 'bookings'
    id = db.Column(db.Integer, primary_key=True)
    client_name = db.Column(db.String(100), nullable=False)
    client_email = db.Column(db.String(120), nullable=False)
    phone_number = db.Column(db.String(20), nullable=True)
    number_days = db.Column(db.Integer, nullable=False)
    travel_date = db.Column(db.Date, nullable=False)
    tour_type = db.Column(db.String(50), nullable=False)  # New field for tour type
    number_people = db.Column(db.Integer, nullable=False)  # New field for number of people
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Foreign key for tour relationship
    tour_id = db.Column(db.Integer, db.ForeignKey('tours.id'), nullable=False)




class Contact(db.Model):
    __tablename__ = 'contacts'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
