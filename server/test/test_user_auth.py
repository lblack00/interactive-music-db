# This file was written by Lucas Black
import unittest
from unittest.mock import patch, MagicMock
import json
from datetime import datetime, timedelta
from app import app
from werkzeug.security import generate_password_hash

class TestUserAuth(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        with self.app.session_transaction() as sess:
            sess.clear()

    @patch('app.users.check_username_exists')
    @patch('app.users.create_new_user')
    @patch('app.db_utils')
    @patch('app.mail')
    def test_signup_success(self, mock_mail, mock_db_utils, mock_create_user, mock_check_username):
        mock_check_username.return_value = False
        mock_db_utils.return_value.read_data.return_value = []
        mock_create_user.return_value = 123

        test_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'SecurePassword123'
        }

        response = self.app.post(
            '/signup',
            data=json.dumps(test_data),
            content_type='application/json'
        )

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 201)
        self.assertIn('message', data)
        self.assertIn('User created successfully', data['message'])
        self.assertTrue(data['requiresVerification'])

        mock_check_username.assert_called_once_with('testuser')
        mock_create_user.assert_called_once()


    @patch('app.users.check_username_exists')
    def test_signup_username_exists(self, mock_check_username):
        mock_check_username.return_value = True

        test_data = {
            'username': 'existinguser',
            'email': 'test@example.com',
            'password': 'SecurePassword123'
        }

        response = self.app.post(
            '/signup',
            data=json.dumps(test_data),
            content_type='application/json'
        )

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 409)
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Username already exists')

    @patch('app.users.check_username_exists')
    @patch('app.db_utils')
    def test_signup_email_exists(self, mock_db_utils, mock_check_username):
        mock_check_username.return_value = False
        mock_db_utils.return_value.read_data.return_value = [{'id': 1}]

        test_data = {
            'username': 'newuser',
            'email': 'existing@example.com',
            'password': 'SecurePassword123'
        }

        response = self.app.post(
            '/signup',
            data=json.dumps(test_data),
            content_type='application/json'
        )

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 409)
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Email address already registered')

    def test_signup_missing_fields(self):
        test_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': ''
        }

        response = self.app.post(
            '/signup',
            data=json.dumps(test_data),
            content_type='application/json'
        )

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Missing fields')

    @patch('app.users.check_username_exists')
    @patch('app.db_utils')
    @patch('app.users.create_new_user')
    def test_signup_server_error(self, mock_create_user, mock_db_utils, mock_check_username):
        mock_check_username.return_value = False
        mock_db_utils.return_value.read_data.return_value = []
        mock_create_user.return_value = None

        test_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'SecurePassword123'
        }

        response = self.app.post(
            '/signup',
            data=json.dumps(test_data),
            content_type='application/json'
        )

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 500)
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Failed to create user')


    @patch('app.is_login_blocked')
    @patch('app.users.get_user')
    @patch('app.check_password_hash')
    @patch('app.reset_login_attempts')
    @patch('app.log_security_event')
    @patch('app.db_utils')
    def test_login_success(self, mock_db_utils, mock_log_event, mock_reset, mock_check_pw, mock_get_user, mock_blocked):
        mock_blocked.return_value = (False, 0)
        mock_get_user.return_value = [{
            'id': 123,
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'hashed_password'
        }]
        mock_check_pw.return_value = True
        mock_db_utils.return_value.read_data.return_value = [{'is_verified': True}]

        test_data = {
            'username': 'testuser',
            'password': 'correctpassword'
        }

        response = self.app.post(
            '/login',
            data=json.dumps(test_data),
            content_type='application/json'
        )

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertIn('message', data)
        self.assertEqual(data['message'], 'Login successful')

        with self.app.session_transaction() as sess:
            self.assertIn('user', sess)
            self.assertEqual(sess['user']['username'], 'testuser')

        mock_reset.assert_called_once()
        mock_log_event.assert_called_once()

    @patch('app.is_login_blocked')
    def test_login_too_many_attempts(self, mock_blocked):
        mock_blocked.return_value = (True, 300)

        test_data = {
            'username': 'testuser',
            'password': 'password'
        }

        response = self.app.post(
            '/login',
            data=json.dumps(test_data),
            content_type='application/json'
        )

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 429)
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Too many failed login attempts')
        self.assertIn('lockout_remaining', data)
        self.assertEqual(data['lockout_remaining'], 300)

    @patch('app.is_login_blocked')
    @patch('app.users.get_user')
    @patch('app.record_failed_login')
    def test_login_user_not_found(self, mock_record_failed, mock_get_user, mock_blocked):
        mock_blocked.return_value = (False, 0)
        mock_get_user.return_value = []

        test_data = {
            'username': 'nonexistentuser',
            'password': 'password'
        }

        response = self.app.post(
            '/login',
            data=json.dumps(test_data),
            content_type='application/json'
        )

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Invalid credentials')
        mock_record_failed.assert_called_once()

    @patch('app.is_login_blocked')
    @patch('app.users.get_user')
    @patch('app.check_password_hash')
    @patch('app.record_failed_login')
    @patch('app.db_utils')
    def test_login_wrong_password(self, mock_db_utils, mock_record_failed, mock_check_pw, mock_get_user, mock_blocked):
        mock_blocked.return_value = (False, 0)
        mock_get_user.return_value = [{
            'id': 123,
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'hashed_password'
        }]
        mock_check_pw.return_value = False
        mock_db_utils.return_value.read_data.return_value = [{'is_verified': True}]

        test_data = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }

        response = self.app.post(
            '/login',
            data=json.dumps(test_data),
            content_type='application/json'
        )

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Invalid credentials')
        mock_record_failed.assert_called_once()

    @patch('app.is_login_blocked')
    @patch('app.users.get_user')
    @patch('app.db_utils')
    def test_login_email_not_verified(self, mock_db_utils, mock_get_user, mock_blocked):
        mock_blocked.return_value = (False, 0)
        mock_get_user.return_value = [{
            'id': 123,
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'hashed_password'
        }]
        mock_db_utils.return_value.read_data.return_value = [{'is_verified': False}]

        with patch('app.CHECK_EMAIL_VERIFICATION', True):
            test_data = {
                'username': 'testuser',
                'password': 'password'
            }

            response = self.app.post(
                '/login',
                data=json.dumps(test_data),
                content_type='application/json'
            )

            data = json.loads(response.data)

            self.assertEqual(response.status_code, 403)
            self.assertIn('error', data)
            self.assertEqual(data['error'], 'Please verify your email before logging in')


    @patch('app.get_client_identifier')
    @patch('app.log_security_event')
    def test_logout(self, mock_log_event, mock_get_ip):
        mock_get_ip.return_value = '127.0.0.1'

        with self.app.session_transaction() as sess:
            sess['user'] = {
                'id': 123,
                'username': 'testuser',
                'email': 'test@example.com'
            }

        response = self.app.post('/logout')

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertIn('message', data)
        self.assertEqual(data['message'], 'Logged out successfully')

        with self.app.session_transaction() as sess:
            self.assertNotIn('user', sess)

        mock_log_event.assert_called_once()

    def test_logout_no_session(self):
        response = self.app.post('/logout')

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertIn('message', data)
        self.assertEqual(data['message'], 'Logged out successfully')


    def test_check_session_logged_in(self):
        with self.app.session_transaction() as sess:
            sess['user'] = {
                'id': 123,
                'username': 'testuser',
                'email': 'test@example.com'
            }

        response = self.app.get('/check-session')

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['logged_in'])
        self.assertIn('user', data)
        self.assertEqual(data['user']['username'], 'testuser')

    def test_check_session_logged_out(self):
        response = self.app.get('/check-session')

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(data['logged_in'])

    def test_is_session_user_match_by_id(self):
        with self.app.session_transaction() as sess:
            sess['user'] = {
                'id': 123,
                'username': 'testuser',
                'email': 'test@example.com'
            }

        response = self.app.get('/is-session-user?identifier=123&type=id')

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['logged_in'])
        self.assertTrue(data['match'])

    def test_is_session_user_no_match_by_id(self):
        with self.app.session_transaction() as sess:
            sess['user'] = {
                'id': 123,
                'username': 'testuser',
                'email': 'test@example.com'
            }

        response = self.app.get('/is-session-user?identifier=456&type=id')

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['logged_in'])
        self.assertFalse(data['match'])

    def test_is_session_user_match_by_username(self):
        with self.app.session_transaction() as sess:
            sess['user'] = {
                'id': 123,
                'username': 'testuser',
                'email': 'test@example.com'
            }

        response = self.app.get('/is-session-user?identifier=testuser&type=username')

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['logged_in'])
        self.assertTrue(data['match'])

    def test_is_session_user_not_logged_in(self):
        response = self.app.get('/is-session-user?identifier=123&type=id')

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(data['logged_in'])
        self.assertFalse(data['match'])

if __name__ == '__main__':
    unittest.main()