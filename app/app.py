from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Space(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)

@app.route('/add_space', methods=['POST'])
def add_space():
    data = request.json
    name = data.get('name')
    description = data.get('description')
    
    if not name:
        return jsonify({'message': 'Name is required'}), 400

    space = Space(name=name, description=description)
    db.session.add(space)
    db.session.commit()
    
    return jsonify({'message': 'Space added successfully'}), 201

@app.route('/spaces')
def view_spaces():
    spaces = Space.query.all()
    space_data = [{'id': space.id, 'name': space.name, 'description': space.description} for space in spaces]
    return jsonify(space_data)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), nullable=False)

@app.route('/add_user', methods=['POST'])
def add_user():
    data = request.json
    username = data.get('username')
    role = data.get('role')
    
    if not username or not role:
        return jsonify({'message': 'Username and role are required'}), 400

    user = User(username=username, role=role)
    db.session.add(user)
    db.session.commit()
    
    return jsonify({'message': 'User added successfully'}), 201

@app.route('/users')
def view_users():
    users = User.query.all()
    user_data = [{'id': user.id, 'username': user.username, 'role': user.role} for user in users]
    return jsonify(user_data)

if __name__ == '__main__':
    app.run(debug=True)
