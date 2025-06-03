from app import app, db
from app.models import Admin

with app.app_context():
    admin = Admin.query.filter_by(email="info@allthings-socotra.com").first()
    if admin:
        admin.is_active = True
        db.session.commit()
        print("Admin account activated.")
    else:
        print("Admin not found.")