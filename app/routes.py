
from flask import render_template, url_for, flash, redirect
from app import app, db, bcrypt
from app.forms import RegistrationForm, LoginForm, ContactForm, BookingForm
from app.models import Admin, Tour,Contact,Booking
from flask_login import login_user, current_user, logout_user,login_required
from flask import request

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/adminregsitration", methods=['GET', 'POST'])
def adminregsitration():
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



@app.route("/adminlogin", methods=['GET', 'POST'])
def adminlogin():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(email=form.email.data).first()
        if admin and bcrypt.check_password_hash(admin.password, form.password.data):
            login_user(admin, remember=form.remember.data)
            next_page = request.args.get('next')  # Ensure this works correctly
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/adminlogout", methods=['GET', 'POST'])
def adminlogout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    return render_template('account.html', title='Account')


@app.route("/contact", methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        # Store the submitted data in the database
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

@app.route('/tour', methods=['GET', 'POST'])
def tour():
    form = BookingForm()

    # Populate the tour_id select field dynamically from the database
    form.tour_id.choices = [(tour.id, tour.title) for tour in Tour.query.all()]

    if form.validate_on_submit():
        # Get the tour instance selected by the user
        tour = Tour.query.get(form.tour_id.data)

        # Create a new Booking instance with the form data
        new_booking = Booking(
            client_name=form.client_name.data,
            client_email=form.client_email.data,
            phone_number=form.phone_number.data,
            country_code=form.country_code.data,
            travel_date=form.travel_date.data,
            number_nights=int(form.number_nights.data),
            number_people=int(form.number_people.data),
            tour_type=form.tour_type.data,
            tour_id=tour.id  # Associate the booking with the selected tour
        )

        # Add the new booking to the session and commit to the database
        db.session.add(new_booking)
        db.session.commit()

        return redirect(url_for('success'))  # Redirect to a success page

    return render_template('tour.html', form=form)

