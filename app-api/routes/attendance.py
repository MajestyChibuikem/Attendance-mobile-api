import json
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import date, datetime

# Path to attendance file
ATTENDANCE_FILE = 'attendance.txt'

# Helper functions for file handling
def load_attendance():
    try:
        with open(ATTENDANCE_FILE, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_attendance(records):
    with open(ATTENDANCE_FILE, 'w') as file:
        json.dump(records, file, indent=4)

# Load attendance initially
ATTENDANCE_RECORDS = load_attendance()

Attendance_blueprint = Blueprint('attendance', __name__)

@Attendance_blueprint.route('/mark', methods=['POST'])
@jwt_required()
def mark_attendance():
    """
    Marks attendance for the logged-in user for a specific date.
    """
    data = request.json
    username = get_jwt_identity()
    attendance_date = data.get('date', str(date.today()))
    status = data.get('status', 'Present')

    # Validate date format
    try:
        attendance_date = datetime.strptime(attendance_date, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400

    # Reload records in case of concurrent changes
    attendance_records = load_attendance()

    # Check if attendance already exists
    for record in attendance_records:
        if record['username'] == username and record['date'] == attendance_date.isoformat():
            return jsonify({'error': 'Attendance already marked for this day'}), 400

    # Add attendance record
    record = {
        'username': username,
        'date': attendance_date.isoformat(),
        'status': status
    }
    attendance_records.append(record)
    save_attendance(attendance_records)

    return jsonify({'message': 'Attendance marked successfully!', 'record': record}), 201

@Attendance_blueprint.route('/records', methods=['GET'])
@jwt_required()
def get_attendance():
    """
    Retrieve attendance records for the logged-in user.
    """
    username = get_jwt_identity()
    start_date = request.args.get('start_date', '2024-01-01')
    end_date = request.args.get('end_date', str(date.today()))

    # Validate date format
    try:
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400

    # Reload attendance records
    attendance_records = load_attendance()

    # Filter attendance records
    user_records = [
        record for record in attendance_records
        if record['username'] == username and start_date <= datetime.strptime(record['date'], '%Y-%m-%d').date() <= end_date
    ]

    return jsonify(user_records), 200
