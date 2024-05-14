from app import app, db
from models import Space, User

def seed():
    with app.app_context():
        # Drop all existing tables
        db.drop_all()

        # Create all tables
        db.create_all()

        # Add example spaces
        space1 = Space(spacename='Meeting Room 1', building='Main Building', floor='2nd Floor', capacity=10, amenities='Projector, Whiteboard')
        space2 = Space(spacename='Conference Room A', building='North Building', floor='3rd Floor', capacity=20, amenities='Projector, Whiteboard, Video Conferencing')
        db.session.add_all([space1, space2])

        # Add example users
        user1 = User(username='admin', role='admin')
        user2 = User(username='viewer', role='viewer')
        db.session.add_all([user1, user2])

        # Commit changes
        db.session.commit()

if __name__ == '__main__':
    seed()
