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

        # Add Beach Lover tour
        beach_lover_tour = Tour(
            title="Beach Lover",
            description="For those who dream of relaxing by the shore, this tour takes you to the most beautiful beaches. Soak up the sun and unwind in paradise.",
            price=800.00,
            status=TourStatusEnum.AVAILABLE,  # Use the Enum status
            number_person=15,  # Customize the max number of people if needed
            admin_id=1  # Make sure to replace this with the actual admin ID
        )
        db.session.add(beach_lover_tour)

        # Add The Explorer tour
        explorer_tour = Tour(
            title="The Explorer",
            description="For those with a thirst for adventure, this tour takes you to the hidden gems and uncharted territories. Get ready for a thrilling journey.",
            price=1000.00,
            status=TourStatusEnum.AVAILABLE,  # Use the Enum status
            number_person=12,  # Customize the max number of people if needed
            admin_id=1  # Make sure to replace this with the actual admin ID
        )
        db.session.add(explorer_tour)

        # Add The Photographer tour
        photographer_tour = Tour(
            title="The Photographer",
            description="Capture the beauty of the world through your lens. Join us on this photographic tour designed for those passionate about photography.",
            price=900.00,
            status=TourStatusEnum.AVAILABLE,  # Use the Enum status
            number_person=8,  # Customize the max number of people if needed
            admin_id=1  # Make sure to replace this with the actual admin ID
        )
        db.session.add(photographer_tour)

        # Commit the changes to the database
        db.session.commit()

        print("✅ Tours added successfully!")

if __name__ == "__main__":
    add_tours()
