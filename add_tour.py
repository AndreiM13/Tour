from app import app, db
from app.models import Tour, TourStatusEnum

def add_tours():
    with app.app_context():
        # Add the VIP tour
        vip_tour = Tour(
            title="The VIP",
            description="You are the boss, determined and adventurous but enjoy comfort. Customize your itinerary with a private consultation to make the tour exactly what you want.",
            price=1200.00,
            status=TourStatusEnum.AVAILABLE,  # Use the Enum status
            number_person=10,  # Customize the max number of people if needed
            admin_id=1  # Make sure to replace this with the actual admin ID
        )
        db.session.add(vip_tour)

        # Commit the changes to the database
        db.session.commit()

        print("✅ Tours added successfully!")

if __name__ == "__main__":
    add_tours()
