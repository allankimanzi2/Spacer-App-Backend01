from flask import Flask, request, jsonify
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from flask_migrate import Migrate
from datetime import timedelta
from models import db, User, Space, Booking
from config import DATABASE_CONFIG  # Import the config
import secrets


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{DATABASE_CONFIG['user']}:{DATABASE_CONFIG['pw']}@{DATABASE_CONFIG['host']}:{DATABASE_CONFIG['port']}/{DATABASE_CONFIG['db']}"

# Generate a random secret key
jwt_secret_key = secrets.token_hex(32)  # Generate a 32-byte (256-bit) random key

# Set the JWT_SECRET_KEY in your Flask app's configuration
app.config['JWT_SECRET_KEY'] = jwt_secret_key

# Initialize extensions
db.init_app(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# URL Routing
@app.route('/')
def index():
    return "This is a basic Flask application"

# Admin Login Route with JWT Authentication
@app.route('/adminlogin', methods=['POST'])
def adminlogin():
    data = request.get_json()

    # Check login credentials
    if data['email'] == 'admin@gmail.com' and data['password'] == 'password':
        expiration_time = timedelta(hours=1)
        token = create_access_token(identity=data['email'], expires_delta=expiration_time)

        return jsonify({"success": True, "message": "Login successful", "token": token, 'user_email': data['email'], 'role': 'admin'}), 200
    else:
        return jsonify({"success": False, "message": "Invalid credentials"}), 401

# Add Space Route
@app.route('/spaces', methods=['POST'])
def add_space():
    data = request.get_json()
    new_space = Space(name=data['name'], description=data['description'], location=data['location'], price_per_hour=data['price_per_hour'], owner_id=data['owner_id'])
    db.session.add(new_space)
    db.session.commit()
    return jsonify({"success": True, "message": "Space added successfully"}), 201

# View All Spaces Route
@app.route('/spaces', methods=['GET'])
def get_spaces():
    spaces = Space.query.all()
    space_list = []
    for space in spaces:
        space_data = {
            'id': space.id,
            'name': space.name,
            'description': space.description,
            'location': space.location,
            'price_per_hour': str(space.price_per_hour),  # Convert to string for JSON compatibility
            'owner_id': space.owner_id,
            'created_at': str(space.created_at)  # Convert to string for JSON compatibility
        }
        space_list.append(space_data)
    return jsonify({"success": True, "spaces": space_list}), 200

# URL Route for adding a new user
@app.route('/users', methods=['POST'])
def add_user():
    data = request.get_json()
    new_user = User(username=data['username'], email=data['email'], password=data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"success": True, "message": "User added successfully"}), 201

# URL Route for getting all users
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    user_list = []
    for user in users:
        user_data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role  # Include 'role' in the response
        }
        user_list.append(user_data)
    return jsonify({"success": True, "users": user_list}), 200



# Add Booking Route
@app.route('/bookings', methods=['POST'])
def add_booking():
    data = request.get_json()
    new_booking = Booking(user_id=data['user_id'], space_id=data['space_id'], start_time=data['start_time'], end_time=data['end_time'], status=data.get('status', 'pending'), payment_status=data.get('payment_status', 'unpaid'))
    db.session.add(new_booking)
    db.session.commit()
    return jsonify({"success": True, "message": "Booking added successfully"}), 201

# View All Bookings Route
@app.route('/bookings', methods=['GET'])
def get_bookings():
    bookings = Booking.query.all()
    booking_list = []
    for booking in bookings:
        booking_data = {
            'id': booking.id,
            'user_id': booking.user_id,
            'space_id': booking.space_id,
            'start_time': str(booking.start_time),  # Convert to string for JSON compatibility
            'end_time': str(booking.end_time),  # Convert to string for JSON compatibility
            'status': booking.status,
            'payment_status': booking.payment_status,
            'created_at': str(booking.created_at)  # Convert to string for JSON compatibility
        }
        booking_list.append(booking_data)
    return jsonify({"success": True, "bookings": booking_list}), 200


if __name__ == '__main__':
    app.run(debug=True)
