import json
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash

# Path to users file
USERS_FILE = 'users.txt'

# Helper functions for file handling
def load_users():
    try:
        with open(USERS_FILE, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_users(users):
    with open(USERS_FILE, 'w') as file:
        json.dump(users, file, indent=4)

# Load users initially
USERS = load_users()

user_blueprint = Blueprint('users', __name__)

@user_blueprint.route('/register', methods=['POST'])
def register():
    """
    Register a new user and store it in the users.txt file.
    """
    data = request.json
    username = data.get('username')
    password = data.get('password')
    device_key = data.get('device_key')

    if not username or not password or not device_key:
        return jsonify({'error': 'All fields are required'}), 400

    # Reload users in case of concurrent changes
    users = load_users()

    # Check for duplicate user
    for user in users:
        if user['username'] == username:
            return jsonify({'error': 'User already exists'}), 401

    hashed_password = generate_password_hash(password)
    user = {
        'username': username,
        'password': hashed_password,
        'device_key': device_key
    }
    users.append(user)
    save_users(users)

    return jsonify({'message': 'User registered successfully!', 'user': user}), 201
