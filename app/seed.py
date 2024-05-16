from app import app, db
from models import Space, User, Booking, Payment
from datetime import datetime

def seed_data():
    with app.app_context():
        # Create Spaces
        space1 = Space(name='Space 1', description='Description of Space 1')
        space2 = Space(name='Space 2', description='Description of Space 2')

        # Create Users
        user1 = User(username='user1', role='role1')
        user2 = User(username='user2', role='role2')

        # Commit objects to database
        db.session.add_all([space1, space2, user1, user2])
        db.session.commit()

        # Create Bookings
        booking1 = Booking(user_id=user1.id, space_id=space1.id, start_time=datetime.now(), end_time=datetime.now(), total_cost=100.0)
        booking2 = Booking(user_id=user2.id, space_id=space2.id, start_time=datetime.now(), end_time=datetime.now(), total_cost=150.0)

        # Create Payments
        payment1 = Payment(booking_id=booking1.id, amount=50.0, from_user_id=user1.id, to_user_id=user2.id, date=datetime.now(), note='Payment for booking 1')
        payment2 = Payment(booking_id=booking2.id, amount=75.0, from_user_id=user2.id, to_user_id=user1.id, date=datetime.now(), note='Payment for booking 2')



if __name__ == '__main__':
    seed_data()
