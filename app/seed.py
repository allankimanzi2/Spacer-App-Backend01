from app import app, db
from models import Space, User, Booking
from datetime import datetime

def seed():
    with app.app_context():
        db.create_all()

        
        # Add Spaces
        space1 = Space(name='Meeting Room 1', description='Small meeting room')
        space2 = Space(name='Conference Hall', description='Large conference hall')
        db.session.add_all([space1, space2])

        # Add users
        user1 = User(username='admin', role='admin')
        user2 = User(username='user1', role='viewer')
        db.session.add_all([user1, user2])

        # Add Bookings
        booking1 = Booking(user_id=1, space_id=1, start_time=datetime(2024, 5, 15, 9, 0), end_time=datetime(2024, 5, 15, 11, 0), total_cost=50.0)
        booking2 = Booking(user_id=2, space_id=2, start_time=datetime(2024, 5, 16, 10, 0), end_time=datetime(2024, 5, 16, 12, 0), total_cost=100.0)
        db.session.add_all([booking1, booking2])


        db.session.commit()


if __name__ == '__main__':
    seed()
