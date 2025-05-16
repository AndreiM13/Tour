from app import app, db
from app.models import Tour, Departure, TourStatusEnum
import datetime

def add_tours_and_departures():
    with app.app_context():
        # VIP
        vip = Tour(title="The VIP", description="…", price=1200.00,
                   status=TourStatusEnum.AVAILABLE, admin_id=1)
        db.session.add(vip)
        db.session.commit()

        for d in (datetime.date(2025,6,1), datetime.date(2025,7,1)):
            db.session.add(Departure(tour_id=vip.id, date=d, max_capacity=10, spots_left=10))

        # Explorer
        exp = Tour(title="The Explorer", description="…", price=950.00,
                   status=TourStatusEnum.AVAILABLE, admin_id=1)
        db.session.add(exp)
        db.session.commit()

        for d in (datetime.date(2025,6,15), datetime.date(2025,7,15)):
            db.session.add(Departure(tour_id=exp.id, date=d, max_capacity=8, spots_left=8))

        # Photographer
        pho = Tour(title="The Photographer", description="…", price=1050.00,
                   status=TourStatusEnum.AVAILABLE, admin_id=1)
        db.session.add(pho)
        db.session.commit()

        for d in (datetime.date(2025,6,10), datetime.date(2025,7,10)):
            db.session.add(Departure(tour_id=pho.id, date=d, max_capacity=6, spots_left=6))

        # Beach Lover
        bl = Tour(title="Beach Lover", description="…", price=800.00,
                  status=TourStatusEnum.AVAILABLE, admin_id=1)
        db.session.add(bl)
        db.session.commit()

        for d in (datetime.date(2025,6,20), datetime.date(2025,7,20)):
            db.session.add(Departure(tour_id=bl.id, date=d, max_capacity=12, spots_left=12))

        db.session.commit()
        print("✅ All tours & departures added!")

if __name__ == "__main__":
    add_tours_and_departures()
