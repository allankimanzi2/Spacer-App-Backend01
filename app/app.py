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
    payments = db.relationship('Payment', backref='booking', lazy=True)

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('booking.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    from_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    to_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    note = db.Column(db.String(255))


@app.route('/book_space', methods=['POST'])
def book_space():
    data = request.json
    user_id = data.get('user_id')
    space_id = data.get('space_id')
    start_time = datetime.strptime(data.get('start_time'), '%Y-%m-%d %H:%M:%S')
    end_time = datetime.strptime(data.get('end_time'), '%Y-%m-%d %H:%M:%S')
    total_cost = data.get('total_cost')
    payment_amount = data.get('payment_amount')
    from_user_id = data.get('from_user_id')
    to_user_id = data.get('to_user_id')
    payment_date = datetime.strptime(data.get('payment_date'), '%Y-%m-%d %H:%M:%S')
    payment_note = data.get('payment_note')

    booking = Booking(user_id=user_id, space_id=space_id, start_time=start_time, end_time=end_time, total_cost=total_cost)
    db.session.add(booking)
    
    payment = Payment(booking_id=booking.id, amount=payment_amount, from_user_id=from_user_id, to_user_id=to_user_id, date=payment_date, note=payment_note)
    db.session.add(payment)
    
    db.session.commit()

    return jsonify({'message': 'Booking and payment added successfully'}), 201

@app.route('/bookings')
def view_bookings():
    bookings = Booking.query.all()
    booking_data = [{'id': booking.id, 'user_id': booking.user_id, 'space_id': booking.space_id, 'start_time': booking.start_time.strftime('%Y-%m-%d %H:%M:%S'), 'end_time': booking.end_time.strftime('%Y-%m-%d %H:%M:%S'), 'total_cost': booking.total_cost} for booking in bookings]
    return jsonify(booking_data)

if __name__ == '__main__':
    app.run(debug=True)
