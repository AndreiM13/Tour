from flask import render_template, url_for, flash, redirect, request, session
from app import app, db, bcrypt
from app.forms import RegistrationForm, LoginForm, ContactForm, BookingForm
from app.models import Admin, Tour, Contact, Booking, BookingStatusEnum, UniqueView,  Departure 
from flask_login import login_user, current_user, logout_user, login_required
from collections import defaultdict
import matplotlib
matplotlib.use('Agg')  # Use the non-GUI backend
import matplotlib.pyplot as plt
import io
import base64
import json
# from flask_mail import Message
# from app import mail  # Assuming 'mail' is imported from your app


#Home Route
@app.route("/")
@app.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    per_page = 5

    pagination = Departure.query.join(Tour).order_by(Departure.date).paginate(page=page, per_page=per_page)

    for dep in pagination.items:
        dep.spots_left = dep.calculate_spots_left()

    tour_title = request.args.get('tour_title', '')

    return render_template("home.html", departures=pagination, tour_title=tour_title)



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
        flash(f'Account created for {form.email.data}!', 'success')
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
    
    # ❌ Removed: form.departure_id.choices = ...

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
    # ❌ Removed: form.departure_id.data = int(preselected_departure_id)

    if request.method == "POST":
        # ✅ Manually retrieve departure ID from hidden field
        departure_id_raw = request.form.get("departure_id")
        try:
            departure_id = int(departure_id_raw)
        except (TypeError, ValueError):
            flash("Invalid or missing departure date.", "danger")
            return redirect(url_for('tour'))

        selected_departure = Departure.query.get(departure_id)
        # Fix: convert datetime.datetime to datetime.date for comparison
        if not selected_departure or selected_departure.date.date() < date.today():
            flash("Selected departure date is invalid or in the past.", "danger")
            return redirect(url_for('tour'))

        if form.validate_on_submit():
            # Find all available tours
            available_tours = Tour.query.filter_by(status="available").all()

            if not available_tours:
                flash('No available tours. Please add a tour first.', 'danger')
                return redirect(url_for('home'))

            # For simplicity, let's select the first available tour
            available_tour = available_tours[0]

            # Automatically select the first admin (assuming admin exists)
            admin = Admin.query.first()

            # If no admin is found, show an error
            if not admin:
                flash('No admin found. Please add an admin first.', 'danger')
                return redirect(url_for('home'))

            # ✅ Use manually validated `selected_departure`
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
                departure_id=selected_departure.id   # <---- add this line
            )


            try:
                db.session.add(new_booking)  # Add the new booking to the session
                db.session.commit()  # Commit the changes to the database

                # Send email to admin notifying about the new booking
                # admin_email = "admin@example.com"  # Replace with actual admin email
                # admin_msg = Message("New Booking Received", recipients=[admin_email])
                # admin_msg.body = f"""New booking received!
                # ...
                # """
                # mail.send(admin_msg)

                # Send personalized confirmation email to the client
                # client_msg = Message("Your Booking Confirmation", recipients=[form.client_email.data])
                # client_msg.body = f"""Dear {form.client_name.data},
                # ...
                # """
                # mail.send(client_msg)

                flash('Booking successful! A confirmation email has been sent to you.', 'success')
                return redirect(url_for('success'))

            except Exception as e:
                db.session.rollback()  # Rollback the session in case of an error
                # print("Booking error:", e) #delete this
                flash('An error occurred while processing your booking. Please try again later.', 'danger')
                return redirect(url_for('tour'))

    # Pass available_dates, departures_json, and tour_title to template for calendar control and JS
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
def cancel_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    booking.status = BookingStatusEnum.CANCELED
    db.session.commit()
    flash('Booking has been canceled.', 'danger')
    return redirect(url_for('account'))

#Delete Booking
@app.route('/delete_booking/<int:booking_id>', methods=['GET'])
@login_required
def delete_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    db.session.delete(booking)
    db.session.commit()
    flash('Booking deleted successfully!', 'danger')
    return redirect(url_for('account'))


#Delete All Bookings
@app.route('/delete_all_bookings', methods=['POST'])
@login_required
def delete_all_bookings():
    Booking.query.delete()
    db.session.commit()
    flash('All bookings deleted successfully!', 'danger')
    return redirect(url_for('account'))




@app.route('/tour/photographer')
def photographer_tour():
    return render_template('tour_trakking.html')

@app.route('/tour/explorer')
def explorer_tour():
    return render_template('tour_explorer.html')

@app.route('/tour/beach-potato')
def beach_potato_tour():
    return render_template('tour_beach_potato.html')

@app.route('/tour/vip')
def vip_tour():
    return render_template('tour_vip.html')
