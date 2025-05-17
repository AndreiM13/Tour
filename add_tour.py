from app import app, db
from app.models import Tour, Departure, TourStatusEnum
import datetime

def add_tours_and_departures():
    with app.app_context():
        # VIP
        vip = Tour(
            title="The VIP",
            description="…",
            price=1200.00,
            tour_type="vip",  # ⬅️ required
            status=TourStatusEnum.AVAILABLE,
            admin_id=1
        )
        db.session.add(vip)
        db.session.commit()

        for d in (datetime.date(2025, 6, 1), datetime.date(2025, 7, 1)):
            db.session.add(Departure(tour_id=vip.id, date=d, max_capacity=10, spots_left=10))

        # Full Island Tour (formerly Explorer)
        fit = Tour(
            title="Full Island Tour",
            description="…",
            price=950.00,
            tour_type="explorer",  # ⬅️ updated but same internal code
            status=TourStatusEnum.AVAILABLE,
            admin_id=1
        )
        db.session.add(fit)
        db.session.commit()

        for d in (datetime.date(2025, 6, 15), datetime.date(2025, 7, 15)):
            db.session.add(Departure(tour_id=fit.id, date=d, max_capacity=8, spots_left=8))

        # Trekking Tour (formerly Photographer)
        trek = Tour(
            title="Trekking Tour",
            description="…",
            price=1050.00,
            tour_type="photographer",  # ⬅️ still using "photographer" internally
            status=TourStatusEnum.AVAILABLE,
            admin_id=1
        )
        db.session.add(trek)
        db.session.commit()

        for d in (datetime.date(2025, 6, 10), datetime.date(2025, 7, 10)):
            db.session.add(Departure(tour_id=trek.id, date=d, max_capacity=6, spots_left=6))

        # Beach Lover
        bl = Tour(
            title="Beach Lover",
            description="…",
            price=800.00,
            tour_type="beach",  # ⬅️ required
            status=TourStatusEnum.AVAILABLE,
            admin_id=1
        )
        db.session.add(bl)
        db.session.commit()

        for d in (datetime.date(2025, 6, 20), datetime.date(2025, 7, 20)):
            db.session.add(Departure(tour_id=bl.id, date=d, max_capacity=12, spots_left=12))

        db.session.commit()
        print("✅ All tours & departures added!")

if __name__ == "__main__":
    add_tours_and_departures()
