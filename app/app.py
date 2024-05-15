from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Space(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), nullable=False)

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

@app.route('/book_space', methods=['POST'])
def book_space():
    data = request.json
    user_id = data.get('user_id')
    space_id = data.get('space_id')
    start_time = datetime.strptime(data.get('start_time'), '%Y-%m-%d %H:%M:%S')
    end_time = datetime.strptime(data.get('end_time'), '%Y-%m-%d %H:%M:%S')
    total_cost = data.get('total_cost')

    booking = Booking(user_id=user_id, space_id=space_id, start_time=start_time, end_time=end_time, total_cost=total_cost)
    db.session.add(booking)
    db.session.commit()

    return jsonify({'message': 'Booking added successfully'}), 201

@app.route('/bookings')
def view_bookings():
    bookings = Booking.query.all()
    booking_data = [{'id': booking.id, 'user_id': booking.user_id, 'space_id': booking.space_id, 'start_time': booking.start_time.strftime('%Y-%m-%d %H:%M:%S'), 'end_time': booking.end_time.strftime('%Y-%m-%d %H:%M:%S'), 'total_cost': booking.total_cost} for booking in bookings]
    return jsonify(booking_data)

if __name__ == '__main__':
    app.run(debug=True)
