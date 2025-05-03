from app import app, db

# Use the application context
with app.app_context():
    db.drop_all()
    db.create_all()
    print("✅ Database has been dropped and recreated successfully!")