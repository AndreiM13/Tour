from flask import render_template, url_for, flash, redirect, request, session
from app import app, db, bcrypt
from app.forms import RegistrationForm, LoginForm, ContactForm, BookingForm, RequestResetForm, ResetPasswordForm, ValidateAccountForm
from app.models import Admin, Tour, Contact, Booking, BookingStatusEnum, UniqueView,  Departure 
from flask_login import login_user, current_user, logout_user, login_required
from collections import defaultdict
import matplotlib
matplotlib.use('Agg')  # Use the non-GUI backend
import matplotlib.pyplot as plt
import io
import base64
import json
from math import ceil
from flask_mail import Message
from app import mail  # Assuming 'mail' is imported from your app
from threading import Thread


from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user


def activation_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('adminlogin'))
        if not current_user.is_active:
            flash("Your account is not activated. Contact admin.", "warning")
            return redirect(url_for('adminlogin'))  # Or send to 'pending_activation'
        return f(*args, **kwargs)
    return decorated_function

#Sending emails async
def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)



def send_reset_email(admin):
    token = admin.get_reset_token()
    msg = Message(
        'Password Reset Request',
        sender=app.config['MAIL_USERNAME'],
        recipients=[admin.email]
    )
    msg.body = f'''To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}

If you did not make this request, please ignore this email.
'''
    mail.send(msg)


@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    form = RequestResetForm()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(email=form.email.data).first()
        if admin:
            send_reset_email(admin)
        flash('If your email exists, instructions have been sent.', 'info')
        return redirect(url_for('adminlogin'))
    return render_template('reset_request.html', form=form)

@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    admin = Admin.verify_reset_token(token)
    if not admin:
        flash('Token is invalid or expired.', 'warning')
        return redirect(url_for('reset_request'))
    
    form = ResetPasswordForm()
    if form.validate_on_submit():
        # ✅ Hash the new password securely
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        admin.password = hashed_password
        db.session.commit()
        flash('Your password has been updated!', 'success')
        return redirect(url_for('adminlogin'))  # Changed from 'login' to 'adminlogin' if applicable
    return render_template('reset_token.html', form=form)

@app.route("/validate_admin/<token>")
def validate_admin(token):
    admin = Admin.verify_activation_token(token)
    if admin:
        if not admin.is_active:
            admin.is_active = True
            db.session.commit()
            flash('Admin account validated successfully. You can now log in.', 'success')
        else:
            flash('Account is already activated.', 'info')
    else:
        flash('Invalid or expired token.', 'danger')
    return redirect(url_for('adminlogin'))




#Home Route
@app.route("/")
@app.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    per_page = 5  # Number of unique dates per page

    # Fetch and group departures by date
    all_departures = Departure.query.join(Tour).order_by(Departure.date).all()

    grouped = defaultdict(list)
    for dep in all_departures:
        dep.spots_left = dep.calculate_spots_left()
        grouped[dep.date].append(dep)

    # Sorted list of tuples: (date, [departures_on_date])
    grouped_departures = sorted(grouped.items(), key=lambda x: x[0])

    # Paginate the grouped list
    total_dates = len(grouped_departures)
    total_pages = ceil(total_dates / per_page)
    start = (page - 1) * per_page
    end = start + per_page
    current_page_items = grouped_departures[start:end]

    return render_template(
        "home.html",
        grouped_departures=current_page_items,
        current_page=page,
        total_pages=total_pages
    )



@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/faq")
def faq():
    return render_template('faq.html')


@app.route("/island")
def island():
    return render_template("island/index.html")  # Main island landing page

@app.route("/island/history")
def island_history():
    return render_template("island/history.html")

@app.route("/island/flora")
def island_flora():
    return render_template("island/flora.html")
@app.route("/island/fauna")
def island_fauna():
    return render_template("island/fauna.html")

@app.route("/island/people")
def island_people():
    return render_template("island/people.html")




@app.route("/getting")
def getting():
    return render_template('getting.html')

@app.route("/high")
def high():
    return render_template('high.html')


# Admin Registration
@app.route("/adminregistration", methods=['GET', 'POST'])
def adminregistration():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        admin = Admin(email=form.email.data, password=hashed_password)
        db.session.add(admin)
        db.session.commit()


        flash(f'Account created for {form.email.data}! Please check your email to activate your account.', 'success')
        return redirect(url_for('home'))

    return render_template('registration.html', title='Registration', form=form)


# Admin Login
@app.route("/adminlogin", methods=['GET', 'POST'])
def adminlogin():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(email=form.email.data).first()
        if admin and bcrypt.check_password_hash(admin.password, form.password.data):
            login_user(admin, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login unsuccessful. Please check email and password.', 'danger')

    return render_template('login.html', title='Login', form=form)


# Admin Logout
@app.route("/adminlogout")
@login_required
def adminlogout():
    logout_user()
    return redirect(url_for('home'))

#account
@app.route("/account", methods=['GET'])
@login_required
@activation_required
def account():

    # Load the country data from the JSON file 
    with open('countries.json') as f:
        countries_data = json.load(f)
    # Create a dictionary to map country codes to country names
    country_code_to_name = {country['dial_code']: country['name'] for country in countries_data}

    # Fetch all bookings from the database
    bookings = Booking.query.all()

    # Track unique views using session
    if 'viewed_account' not in session:
        # Mark the session as viewed
        session['viewed_account'] = True

        # Check if a UniqueView entry exists, otherwise create one
        unique_view = UniqueView.query.first()

        if unique_view:
            # Increment the view count
            unique_view.count += 1
        else:
            # Create a new UniqueView entry if it doesn't exist
            unique_view = UniqueView(count=1)
            db.session.add(unique_view)

        # Commit the changes to the database
        db.session.commit()

    # Create a dictionary to hold statistics per country
    country_stats = defaultdict(lambda: {
        'total_people': 0,
        'confirmed': 0,
        'canceled': 0,
    })

    # Loop through the bookings and update statistics
    for booking in bookings:
        country_code = booking.country_code
        country_stats[country_code]['total_people'] += booking.number_people
        
        if booking.status == BookingStatusEnum.CONFIRMED:
            country_stats[country_code]['confirmed'] += booking.number_people
        elif booking.status == BookingStatusEnum.CANCELED:
            country_stats[country_code]['canceled'] += booking.number_people

    # Prepare the data for the chart
    country_names = [country_code_to_name.get(country_code, country_code) for country_code in country_stats.keys()]
    confirmed = [stats["confirmed"] for stats in country_stats.values()]
    canceled = [stats["canceled"] for stats in country_stats.values()]

    # Generate a bar chart for the booking analytics
    fig, ax = plt.subplots(figsize=(10, 6))
    bar_width = 0.35
    index = range(len(country_names))

    # Plotting confirmed and canceled data
    ax.bar(index, confirmed, bar_width, label='Confirmed', color='green')
    ax.bar([i + bar_width for i in index], canceled, bar_width, label='Canceled', color='red')

    ax.set_xlabel('Countries')
    ax.set_ylabel('Number of People')
    ax.set_title('Booking Analytics by Country')
    ax.set_xticks([i + bar_width / 2 for i in index])
    ax.set_xticklabels(country_names, rotation=45, ha='right')
    ax.legend()

    # Save the plot to a BytesIO object and encode it as base64 for embedding in the HTML
    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)
    img_data = base64.b64encode(img.getvalue()).decode('utf-8')

    # Fetch the updated view count from the database
    unique_view = UniqueView.query.first()
    view_count = unique_view.count if unique_view else 0

    # Pass the aggregated data and the image data to the template
    return render_template("account.html", title='Account', bookings=bookings, country_stats=country_stats, img_data=img_data, view_count=view_count)

# Contact Form
@app.route("/contact", methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        contact = Contact(
            name=form.name.data,
            email=form.email.data,
            message=form.message.data
        )
        db.session.add(contact)
        db.session.commit()
        flash("Your message has been sent successfully!", "success")
        return redirect(url_for('contact'))

    return render_template('contact.html', form=form)

# Tour Booking
@app.route('/tour', methods=['GET', 'POST'])
def tour():
    form = BookingForm()

    # Prepare available departure dates from the database (next 14 days or more)
    from datetime import date, timedelta
    upcoming_departures = Departure.query.filter(Departure.date >= date.today()).order_by(Departure.date).all()

    # Optional: fallback for available_dates for front-end use (if still needed)
    available_dates = [
        (date.today() + timedelta(days=i)).strftime('%Y-%m-%d')
        for i in range(1, 15)
    ]

    # Prepare departures JSON for JavaScript use
    departures_json = [
        {"id": dep.id, "date": dep.date.strftime('%Y-%m-%d')}
        for dep in upcoming_departures
    ]

    # Get the tour title from query params (to show on booking page)
    tour_title = request.args.get("tour_title", default="", type=str)

    # Pre-fill the departure_id if coming from homepage with a departure link
    preselected_departure_id = request.args.get("departure_id")

    if request.method == "POST":
        # ✅ Manually retrieve departure ID from hidden field
        departure_id_raw = request.form.get("departure_id")
        try:
            departure_id = int(departure_id_raw)
        except (TypeError, ValueError):
            flash("Invalid or missing departure date.", "danger")
            return redirect(url_for('tour'))

        selected_departure = Departure.query.get(departure_id)
        if not selected_departure or selected_departure.date.date() < date.today():
            flash("Selected departure date is invalid or in the past.", "danger")
            return redirect(url_for('tour'))

        if form.validate_on_submit():
            available_tours = Tour.query.filter_by(status="available").all()
            if not available_tours:
                flash('No available tours. Please add a tour first.', 'danger')
                return redirect(url_for('home'))

            available_tour = available_tours[0]
            admin = Admin.query.first()

            if not admin:
                flash('No admin found. Please add an admin first.', 'danger')
                return redirect(url_for('home'))

            new_booking = Booking(
                client_name=form.client_name.data,
                client_email=form.client_email.data,
                phone_number=form.phone_number.data,
                country_code=form.country_code.data,
                travel_date=selected_departure.date,
                number_nights=form.number_nights.data,
                number_people=form.number_people.data,
                tour_type=form.tour_type.data,
                admin_id=admin.id,
                tour_id=available_tour.id,
                departure_id=selected_departure.id
            )

            try:
                db.session.add(new_booking)
                db.session.commit()

                # Tour type name mapping
                tour_type_names = {
                    "trekking": "Trekking Tour",
                    "full_island": "Full Island Tour",
                    "beach": "Beach Lover Tour",
                    "vip": "The VIP Tour"
                }
                tour_type_display = tour_type_names.get(form.tour_type.data, "Your Selected Tour")

                # Admin email
                admin_email = "info@allthings-socotra.com"
                admin_msg = Message(
                    "New Booking Received",
                    sender=app.config['MAIL_USERNAME'],
                    recipients=[admin_email]
                )
                admin_msg.body = f"""New booking received!

Client Name: {form.client_name.data}
Email: {form.client_email.data}
Phone: {form.phone_number.data}
Country Code: {form.country_code.data}
Tour Type: {form.tour_type.data}
Number of People: {form.number_people.data}
Number of Nights: {form.number_nights.data}
Departure Date: {selected_departure.date.strftime('%Y-%m-%d')}

Please log into the admin panel to view more details.
"""

                # Client email (with formatted tour type name)
                client_msg = Message(
                    "Your Booking Confirmation",
                    sender=app.config['MAIL_USERNAME'],
                    recipients=[form.client_email.data]
                )
                client_msg.html = f"""
                                <html>
                                <body style="font-family: Arial, sans-serif; color: #333;">
                                    <h2 style="color: #2a7ae2;">Thank you for booking your tour with us!</h2>
                                    <p>Dear {form.client_name.data},</p>
                                    <p>Here are your booking details:</p>
                                    <ul>
                                        <li><strong>Tour Type:</strong> {tour_type_display}</li>
                                        <li><strong>Number of People:</strong> {form.number_people.data}</li>
                                        <li><strong>Departure Date:</strong> {selected_departure.date.strftime('%Y-%m-%d')}</li>
                                    </ul>
                                    <p>Please keep an eye on your inbox (and check your spam/junk folder just in case).</p>
                                    <p>You will soon receive a detailed itinerary, pricing information, and any special offers we may have for your tour. 😉</p>
                                    <br>
                                    <p>Best regards,<br><strong>All Things Socotra Team</strong></p>
                                    <img src="https://raw.githubusercontent.com/AndreiM13/Tour/main/app/static/images/logo.png" alt="All Things Socotra Logo" style="margin-top: 10px; height: 40px; width:40px;">
                                </body>
                                </html>
                                """


                # Sending emails asynchronously
                Thread(target=send_async_email, args=(app, admin_msg)).start()
                Thread(target=send_async_email, args=(app, client_msg)).start()

                flash('Booking successful! A confirmation email has been sent to you.', 'success')
                return redirect(url_for('success'))

            except Exception as e:
                db.session.rollback()
                flash('An error occurred while processing your booking. Please try again later.', 'danger')
                return redirect(url_for('tour'))

    return render_template('tour.html',
                           form=form,
                           available_dates=available_dates,
                           departures_json=departures_json,
                           tour_title=tour_title)




# Booking Success Page
@app.route("/success")
def success():
    return render_template("success.html")


#Confirm Booking
@app.route('/confirm_booking/<int:booking_id>', methods=['GET'])
@login_required
@activation_required
def confirm_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    print(f"Booking status: {booking.status}")  # This will log to your console
    if booking.status == BookingStatusEnum.PENDING:
        booking.status = BookingStatusEnum.CONFIRMED
        db.session.commit()
        flash('Booking confirmed successfully!', 'success')
    else:
        flash('Booking is already confirmed or canceled!', 'danger')
    return redirect(url_for('account'))

#Cancel Booking
@app.route("/cancel_booking/<int:booking_id>")
@login_required
@activation_required
def cancel_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    booking.status = BookingStatusEnum.CANCELED
    db.session.commit()
    flash('Booking has been canceled.', 'danger')
    return redirect(url_for('account'))

#Delete Booking
@app.route('/delete_booking/<int:booking_id>', methods=['GET'])
@login_required
@activation_required
def delete_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    db.session.delete(booking)
    db.session.commit()
    flash('Booking deleted successfully!', 'danger')
    return redirect(url_for('account'))


#Delete All Bookings
@app.route('/delete_all_bookings', methods=['POST'])
@login_required
@activation_required
def delete_all_bookings():
    Booking.query.delete()
    db.session.commit()
    flash('All bookings deleted successfully!', 'danger')
    return redirect(url_for('account'))



@app.route('/tour/trekking')
def trekking_tour():
    return render_template('tour_trekking.html')


@app.route('/tour/full-island-tour')
def full_island_tour():
    return render_template('island_tour.html')


@app.route('/tour/beach-lover')
def beach_lover():
    return render_template('beach_lover.html')

@app.route('/tour/vip')
def vip_tour():
    return render_template('tour_vip.html')
