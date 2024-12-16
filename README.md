### Documentation for Flask API Project

#### Project Overview
This Flask API project allows for:
1. **User registration and authentication** (handled in `auth.py` and `users.py`).
2. **Attendance logging** (handled in `attendance.py`).
3. Data persistence using simple text files (`users.txt` and `attendance.txt`).

The API routes are organized in a modular structure within the `routes` folder.

---

### File Descriptions

#### 1. `app.py`
This is the main entry point of the Flask application. It initializes the Flask app, registers the routes, and runs the server.

**Key Components**:
- **Imports**: Required libraries and route modules.
- **Route Initialization**: Registers blueprints from the `routes` folder.
- **Environment Variables**: Loaded from a `.env` file (not shown).

```python
from flask import Flask
from routes.auth import auth_bp
from routes.users import users_bp
from routes.attendance import attendance_bp

app = Flask(__name__)

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(users_bp, url_prefix='/users')
app.register_blueprint(attendance_bp, url_prefix='/attendance')

if __name__ == "__main__":
    app.run(debug=True)
```

---

#### 2. `routes/auth.py`
This file handles **user authentication**.

**Main Routes**:
- **`/auth/login`**: Allows users to log in with their registration number.
- **`/auth/register`**: Handles first-time user registration.

**Key Features**:
- Verifies if the user already exists in `users.txt`.
- Ensures new users provide unique registration numbers.
- Writes user data into `users.txt` for persistence.

**Example Code Snippet**:
```python
from flask import Blueprint, request, jsonify

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    reg_number = request.json.get('reg_number')
    with open('users.txt', 'r') as file:
        users = file.readlines()
    for user in users:
        if reg_number in user:
            return jsonify({"message": "Login successful"}), 200
    return jsonify({"error": "User not found"}), 404
```

---

#### 3. `routes/users.py`
This file handles **user-related functionalities**.

**Main Routes**:
- **`/users/list`**: Lists all registered users.
- **`/users/delete`**: Deletes a user by registration number.

**Key Features**:
- Reads and writes from/to `users.txt`.
- Provides basic CRUD operations for user management.

---

#### 4. `routes/attendance.py`
This file handles **attendance logging**.

**Main Routes**:
- **`/attendance/log`**: Logs attendance for a user.
- **`/attendance/list`**: Lists all attendance logs.

**Key Features**:
- Writes attendance records into `attendance.txt`.
- Captures time of attendance logging.

**Example Code Snippet**:
```python
from flask import Blueprint, request, jsonify
from datetime import datetime

attendance_bp = Blueprint('attendance', __name__)

@attendance_bp.route('/log', methods=['POST'])
def log_attendance():
    reg_number = request.json.get('reg_number')
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open('attendance.txt', 'a') as file:
        file.write(f"{reg_number}, {timestamp}\n")
    return jsonify({"message": "Attendance logged"}), 200
```

---

#### 5. `users.txt`
This file is used to persist user data. Each line represents a user, containing:
- **Name**
- **Registration number**
- **Unique key**

**Example Content**:
```
John Doe, 12345, abc123key
Jane Smith, 67890, xyz456key
```

---

#### 6. `attendance.txt`
This file is used to log attendance records. Each line contains:
- **Registration number**
- **Timestamp**

**Example Content**:
```
12345, 2024-06-10 08:00:00
67890, 2024-06-10 08:05:00
```


---

## 7.  `Unit_tests.py`
This test suite provides a robust testing framework for a Flask-based authentication and attendance tracking API. It covers crucial aspects of the application's functionality, ensuring reliability and correct behavior across different scenarios.
## Test Environment Setup

### Prerequisites
- Python 3.8+
- Flask
- Flask-JWT-Extended
- unittest framework

### Installation
```bash
pip install flask flask-jwt-extended
```

## Test Suite Structure

### Key Components
- **FlaskAPITestCase**: Main test class inheriting from `unittest.TestCase`
- Comprehensive test methods covering various API endpoints
- Temporary file management for isolated testing

### Test Categories

#### 1. User Management Tests
- User Registration
- Duplicate User Prevention
- Login Mechanism
- Invalid Credential Handling

#### 2. Attendance Management Tests
- Attendance Marking
- Duplicate Attendance Prevention
- Attendance Record Retrieval

## Test Methods Breakdown

### User Registration and Authentication Tests

#### `test_user_registration_and_login`
- **Purpose**: Verify user can successfully register and login
- **Steps**:
  1. Register a new user
  2. Attempt login with registered credentials
- **Validations**:
  - Successful registration (HTTP 201)
  - Successful login (HTTP 200)
  - Presence of access and refresh tokens

#### `test_duplicate_user_registration`
- **Purpose**: Prevent multiple registrations with same username
- **Steps**:
  1. Register first user
  2. Attempt to register same user again
- **Validations**:
  - First registration succeeds
  - Second registration fails (HTTP 401)

### Attendance Management Tests

#### `test_attendance_marking`
- **Purpose**: Allow users to mark attendance
- **Steps**:
  1. Register and login user
  2. Mark attendance for current date
- **Validations**:
  - Successful attendance marking (HTTP 201)
  - Correct success message

#### `test_duplicate_attendance_marking`
- **Purpose**: Prevent multiple attendance marks on same day
- **Steps**:
  1. Register and login user
  2. Mark attendance twice on same day
- **Validations**:
  - First attendance mark succeeds
  - Second attendance mark fails (HTTP 400)

#### `test_retrieve_attendance_records`
- **Purpose**: Retrieve user's attendance records
- **Steps**:
  1. Register and login user
  2. Mark multiple attendance records
  3. Retrieve attendance records
- **Validations**:
  - Successfully retrieve records (HTTP 200)
  - Correct number of records returned

### Authentication Failure Tests

#### `test_login_invalid_credentials`
- **Purpose**: Handle invalid login attempts
- **Scenarios**:
  1. Login with incorrect password
  2. Login with non-existent user
- **Validations**:
  - Both scenarios result in authentication failure (HTTP 401)

## Test Environment Management

### File Handling
- Temporary files used to prevent data modification
- Automatic cleanup after each test
- Isolated test environment for each test method

### JWT Authentication
- Test-specific secret key
- Token generation and validation
- Mocking authentication flow

## Best Practices

### Running Tests
```bash
python -m unittest test_flask_api.py
```
## from this line contains points of improvement for version 2.0!!!

### Debugging Tips
- Check error messages for specific failure points
- Verify test dependencies are correctly installed
- Ensure correct project structure

## Potential Improvements
- Add more edge case scenarios
- Implement more granular error checking
- Consider property-based testing for complex scenarios

## Limitations
- Relies on file-based storage (consider database for production)
- JWT secret key is hardcoded (use environment variables in production)
- Assumes specific application structure


---

### Notes:
- **Blueprints**: Routes are modularized using Flask blueprints for better code organization.
- **File-based Storage**: Data is stored in simple text files (`users.txt` and `attendance.txt`). Consider using a database like SQLite or PostgreSQL for scalability.
- **Error Handling**: Basic error responses are included, but input validation and exception handling can be improved.

---

### Recommendations:
1. **Input Validation**: Use libraries like `marshmallow` or `pydantic` to validate inputs.
2. **Error Handling**: Add try-except blocks for file operations to avoid crashes.
3. **Testing**: Write unit tests for all routes using frameworks like `unittest` or `pytest`.
4. **Security**: Implement API keys, user authentication tokens, or similar security measures.

---

