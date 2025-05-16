from datetime import datetime
from app import db
from flask_login import UserMixin
from sqlalchemy import Enum as SqlEnum
from enum import Enum

# Import login_manager from the app package
from app import login_manager

# Use Enum for status in Tour and Booking
class BookingStatusEnum(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELED = "canceled"

class TourStatusEnum(str, Enum):
    AVAILABLE = "available"
    SOLD_OUT = "sold out"
    IN_PROGRESS = "in progress"

@login_manager.user_loader
def load_user(user_id):
    return Admin.query.get(int(user_id))

class Admin(db.Model, UserMixin):
    __tablename__ = 'admins'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)  # Index added for faster lookups
    password = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    tours = db.relationship('Tour', backref='admin', lazy=True, cascade="all, delete-orphan")
    bookings = db.relationship('Booking', backref='admin', lazy=True, cascade="all, delete-orphan")
    contacts = db.relationship('Contact', backref='admin', lazy=True, cascade="all, delete-orphan")

class Tour(db.Model):
    __tablename__ = 'tours'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    number_person = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(SqlEnum(TourStatusEnum), nullable=False, default=TourStatusEnum.AVAILABLE)

    admin_id = db.Column(db.Integer, db.ForeignKey('admins.id'), nullable=False)
    bookings = db.relationship('Booking', backref='tour', lazy=True, cascade="all, delete-orphan")



class Booking(db.Model):
    __tablename__ = 'bookings'
    id = db.Column(db.Integer, primary_key=True)
    client_name = db.Column(db.String(100), nullable=False)
    client_email = db.Column(db.String(120), nullable=False)
    phone_number = db.Column(db.String(20), nullable=True)
    country_code = db.Column(db.String(10), nullable=True)
    number_nights = db.Column(db.Integer, nullable=False)
    travel_date = db.Column(db.Date, nullable=False)
    tour_type = db.Column(db.String(50), nullable=False)
    number_people = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(SqlEnum(BookingStatusEnum), nullable=False, default=BookingStatusEnum.PENDING)
    tour_id = db.Column(db.Integer, db.ForeignKey('tours.id'), nullable=False)
     # NEW: Link each booking to a specific departure (date + capacity)
    departure_id   = db.Column(db.Integer, db.ForeignKey('departures.id'), nullable=False)
    admin_id = db.Column(db.Integer, db.ForeignKey('admins.id'), nullable=False)

class Contact(db.Model):
    __tablename__ = 'contacts'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False, index=True)  # Index for quicker lookups
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    admin_id = db.Column(db.Integer, db.ForeignKey('admins.id'), nullable=False)

    
class UniqueView(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    count = db.Column(db.Integer, default=0)

class Departure(db.Model):
    __tablename__ = 'departures'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    max_capacity = db.Column(db.Integer, nullable=False)
    spots_left = db.Column(db.Integer, nullable=False)

    tour_id = db.Column(db.Integer, db.ForeignKey('tours.id'), nullable=False)

    # Use the same backref name here, matching the Tour model's departure relationship
    tour = db.relationship('Tour', backref='departures')  # No changes needed here, just make sure the backref exists


    # calculate spots_left dynamically based on bookings
    def calculate_spots_left(self):
        booked_spots = db.session.query(db.func.count(Booking.id)).filter(Booking.departure_id == self.id).scalar()
        return self.max_capacity - booked_spots


    # backref from Tour: Tour.departures
