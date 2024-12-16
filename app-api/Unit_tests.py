import os
import json
import unittest
from datetime import date, datetime, timedelta

from flask import Flask
from flask_jwt_extended import JWTManager, create_access_token

# Import the route registration function
from routes import register_routes

# Temporary test files to avoid modifying real data
TEST_USERS_FILE = 'test_users.txt'
TEST_ATTENDANCE_FILE = 'test_attendance.txt'

# Monkey patch the file paths for testing
import routes.users
import routes.attendance
routes.users.USERS_FILE = TEST_USERS_FILE
routes.attendance.ATTENDANCE_FILE = TEST_ATTENDANCE_FILE

class FlaskAPITestCase(unittest.TestCase):
    def setUp(self):
        """Set up test environment before each test"""
        # Create test Flask app
        self.app = Flask(__name__)
        
        # Configure JWT
        self.app.config['JWT_SECRET_KEY'] = 'test-secret-key'
        self.jwt = JWTManager(self.app)
        
        # Register routes
        register_routes(self.app)
        
        # Create test client
        self.client = self.app.test_client()
        
        # Clear test files before each test
        self._prepare_test_files()

    def tearDown(self):
        """Clean up test environment after each test"""
        self._cleanup_test_files()

    def _prepare_test_files(self):
        """Prepare initial test data files"""
        # Create empty JSON files
        with open(TEST_USERS_FILE, 'w') as f:
            json.dump([], f)
        
        with open(TEST_ATTENDANCE_FILE, 'w') as f:
            json.dump([], f)

    def _cleanup_test_files(self):
        """Remove test data files"""
        for filename in [TEST_USERS_FILE, TEST_ATTENDANCE_FILE]:
            if os.path.exists(filename):
                os.remove(filename)

    def _register_test_user(self, username='testuser', password='testpass', device_key='testkey'):
        """Helper method to register a test user"""
        register_response = self.client.post('/users/register', json={
            'username': username,
            'password': password,
            'device_key': device_key
        })
        return register_response

    def _login_test_user(self, username='testuser', password='testpass'):
        """Helper method to login and get access token"""
        login_response = self.client.post('/auth/login', json={
            'username': username,
            'password': password
        })
        return login_response.json

    def test_user_registration_and_login(self):
        """Test user registration and login flow"""
        # Register user
        register_response = self._register_test_user()
        self.assertEqual(register_response.status_code, 201)
        
        # Login user
        login_response = self.client.post('/auth/login', json={
            'username': 'testuser',
            'password': 'testpass'
        })
        self.assertEqual(login_response.status_code, 200)
        self.assertIn('access token', login_response.json)
        self.assertIn('refresh token', login_response.json)

    def test_duplicate_user_registration(self):
        """Test preventing duplicate user registrations"""
        # First registration should succeed
        self._register_test_user()
        
        # Second registration with same username should fail
        second_register = self._register_test_user()
        self.assertEqual(second_register.status_code, 401)

    def test_attendance_marking(self):
        """Test marking attendance for a logged-in user"""
        # Register and login user
        self._register_test_user()
        login_data = self._login_test_user()
        access_token = login_data['access token']

        # Mark attendance
        attendance_response = self.client.post('/attendance/mark', 
            json={'date': str(date.today())},
            headers={'Authorization': f'Bearer {access_token}'}
        )
        self.assertEqual(attendance_response.status_code, 201)
        self.assertIn('Attendance marked successfully', attendance_response.json['message'])

    def test_duplicate_attendance_marking(self):
        """Test preventing duplicate attendance for same day"""
        # Register and login user
        self._register_test_user()
        login_data = self._login_test_user()
        access_token = login_data['access token']

        # First attendance mark should succeed
        first_mark = self.client.post('/attendance/mark', 
            json={'date': str(date.today())},
            headers={'Authorization': f'Bearer {access_token}'}
        )
        self.assertEqual(first_mark.status_code, 201)

        # Second attendance mark on same day should fail
        second_mark = self.client.post('/attendance/mark', 
            json={'date': str(date.today())},
            headers={'Authorization': f'Bearer {access_token}'}
        )
        self.assertEqual(second_mark.status_code, 400)

    def test_retrieve_attendance_records(self):
        """Test retrieving attendance records"""
        # Register and login user
        self._register_test_user()
        login_data = self._login_test_user()
        access_token = login_data['access token']

        # Mark multiple attendance records
        test_dates = [
            str(date.today() - timedelta(days=i)) 
            for i in range(3)
        ]
        for test_date in test_dates:
            self.client.post('/attendance/mark', 
                json={'date': test_date},
                headers={'Authorization': f'Bearer {access_token}'}
            )

        # Retrieve records
        records_response = self.client.get('/attendance/records', 
            query_string={
                'start_date': str(date.today() - timedelta(days=5)),
                'end_date': str(date.today())
            },
            headers={'Authorization': f'Bearer {access_token}'}
        )
        
        self.assertEqual(records_response.status_code, 200)
        self.assertEqual(len(records_response.json), 3)

    def test_login_invalid_credentials(self):
        """Test login with invalid credentials"""
        # First register a user
        self._register_test_user()

        # Try login with wrong password
        wrong_password_login = self.client.post('/auth/login', json={
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        self.assertEqual(wrong_password_login.status_code, 401)

        # Try login with non-existent user
        non_existent_login = self.client.post('/auth/login', json={
            'username': 'nonexistent',
            'password': 'anypassword'
        })
        self.assertEqual(non_existent_login.status_code, 401)

if __name__ == '__main__':
    unittest.main()