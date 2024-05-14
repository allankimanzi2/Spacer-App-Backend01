from flask_sqlalchemy import SQLAlchemy
from app import db

db = SQLAlchemy()

#Space
class Space(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)

    def __init__(self, name, description):
        self.name = name
        self.description = description


#User 
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(50), nullable=False)

#Booking spaces
class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    space_id = db.Column(db.Integer, db.ForeignKey('space.id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    total_cost = db.Column(db.Float, nullable=False)

    def __init__(self, user_id, space_id, start_time, end_time, total_cost):
        self.user_id = user_id
        self.space_id = space_id
        self.start_time = start_time
        self.end_time = end_time
        self.total_cost = total_cost
