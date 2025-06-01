from app import app, db
from app.models import Tour, Departure, TourStatusEnum
import datetime

def add_tours_and_departures():
    with app.app_context():
        # 2025 dates: Sept–Dec
        dates_2025 = [
            datetime.date(2025, 9, 30),
            datetime.date(2025, 10, 7),
            datetime.date(2025, 10, 14),
            datetime.date(2025, 10, 21),
            datetime.date(2025, 10, 28),
            datetime.date(2025, 11, 4),
            datetime.date(2025, 11, 11),
            datetime.date(2025, 11, 18),
            datetime.date(2025, 11, 25),
            datetime.date(2025, 12, 2),
            datetime.date(2025, 12, 9),
            datetime.date(2025, 12, 16),
            datetime.date(2025, 12, 23),
            datetime.date(2025, 12, 30),
        ]

        # 2026 dates: Jan–Apr
        dates_2026 = [
            datetime.date(2026, 1, 6),
            datetime.date(2026, 1, 13),
            datetime.date(2026, 1, 20),
            datetime.date(2026, 1, 27),
            datetime.date(2026, 2, 3),
            datetime.date(2026, 2, 10),
            datetime.date(2026, 2, 17),
            datetime.date(2026, 2, 24),
            datetime.date(2026, 3, 3),
            datetime.date(2026, 3, 10),
            datetime.date(2026, 3, 17),
            datetime.date(2026, 3, 24),
            datetime.date(2026, 3, 31),
            datetime.date(2026, 4, 7),
            datetime.date(2026, 4, 14),
            datetime.date(2026, 4, 21),
        ]

        all_departure_dates = dates_2025 + dates_2026

        # List of all tour titles
        tour_data = [
           
            {"title": "Full Island Tour", "description": "…", "price": 950.00, "tour_type": "explorer", "capacity": 8},
            {"title": "Trekking Tour", "description": "…", "price": 1050.00, "tour_type": "photographer", "capacity": 6},
            {"title": "Beach Lover", "description": "…", "price": 800.00, "tour_type": "beach", "capacity": 12},
            {"title": "The VIP", "description": "…", "price": 1200.00, "tour_type": "vip", "capacity": 10},
        ]

        # Store tour titles for later display
        created_tours = []

        for tour_info in tour_data:
            tour = Tour(
                title=tour_info["title"],
                description=tour_info["description"],
                price=tour_info["price"],
                tour_type=tour_info["tour_type"],
                status=TourStatusEnum.AVAILABLE,
                admin_id=1
            )
            db.session.add(tour)
            db.session.commit()

            created_tours.append(tour.title)

            for date in all_departure_dates:
                db.session.add(Departure(
                    tour_id=tour.id,
                    date=date,
                    max_capacity=tour_info["capacity"],
                    spots_left=tour_info["capacity"]
                ))

        db.session.commit()
        print("✅ All 2025–2026 tours & departures added!")



if __name__ == "__main__":
    add_tours_and_departures()
