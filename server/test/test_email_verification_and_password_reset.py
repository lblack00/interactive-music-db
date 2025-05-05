# This file was written by Lucas Black
import unittest
import json
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
from flask import Flask
from flask_mail import Message
from app import app

class TestEmailVerificationAndPasswordReset(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.client = self.app.test_client()
        self.app.config['TESTING'] = True

    @patch('app.db_utils')
    def test_verify_email_success(self, mock_db_utils):
        mock_db = MagicMock()
        mock_db.mutate_data.return_value = [{'user_id': 1}]
        mock_db_utils.return_value = mock_db

        response = self.client.get('/verify-email?token=valid_token')

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'Email verified successfully')

        mock_db.mutate_data.assert_called_once()
        call_args = mock_db.mutate_data.call_args[0]
        self.assertIn('UPDATE email_verification', call_args[0])
        self.assertIn('SET is_verified = TRUE', call_args[0])
        self.assertEqual(call_args[1], ('valid_token',))

    @patch('app.db_utils')
    def test_verify_email_missing_token(self, mock_db_utils):
        response = self.client.get('/verify-email')

        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data['error'], 'Missing verification token')

        mock_db_utils.return_value.mutate_data.assert_not_called()

    @patch('app.db_utils')
    def test_verify_email_invalid_token(self, mock_db_utils):
        mock_db = MagicMock()
        mock_db.mutate_data.return_value = []
        mock_db_utils.return_value = mock_db

        response = self.client.get('/verify-email?token=invalid_token')

        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data['error'], 'Invalid or expired verification token')

    @patch('app.db_utils')
    def test_verify_email_exception(self, mock_db_utils):
        mock_db = MagicMock()
        mock_db.mutate_data.side_effect = Exception("Database error")
        mock_db_utils.return_value = mock_db

        response = self.client.get('/verify-email?token=error_token')

        self.assertEqual(response.status_code, 500)
        data = json.loads(response.data)
        self.assertEqual(data['error'], 'Verification failed')

    @patch('app.mail')
    @patch('app.db_utils')
    @patch('app.secrets.token_urlsafe')
    def test_request_password_reset_success(self, mock_token_urlsafe, mock_db_utils, mock_mail):
        mock_token_urlsafe.return_value = 'test_reset_token'

        mock_db = MagicMock()
        mock_db.read_data.return_value = [{'id': 1, 'username': 'testuser'}]
        mock_db.mutate_data.return_value = None
        mock_db_utils.return_value = mock_db

        response = self.client.post(
            '/request-password-reset',
            data=json.dumps({'email': 'test@example.com'}),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'If an account exists with this email, you will receive reset instructions.')

        mock_mail.send.assert_called_once()
        email_message = mock_mail.send.call_args[0][0]
        self.assertIn('test@example.com', email_message.recipients)
        self.assertIn('test_reset_token', email_message.body)

        mock_db.mutate_data.assert_called_once()
        call_args = mock_db.mutate_data.call_args[0]
        self.assertIn('INSERT INTO password_reset_tokens', call_args[0])
        self.assertEqual(call_args[1][0], 1)
        self.assertEqual(call_args[1][1], 'test_reset_token')

    @patch('app.mail')
    @patch('app.db_utils')
    def test_request_password_reset_nonexistent_email(self, mock_db_utils, mock_mail):
        mock_db = MagicMock()
        mock_db.read_data.return_value = []
        mock_db_utils.return_value = mock_db

        response = self.client.post(
            '/request-password-reset',
            data=json.dumps({'email': 'nonexistent@example.com'}),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'If an account exists with this email, you will receive reset instructions.')

        mock_mail.send.assert_not_called()
        mock_db.mutate_data.assert_not_called()

    @patch('app.db_utils')
    def test_request_password_reset_missing_email(self, mock_db_utils):
        response = self.client.post(
            '/request-password-reset',
            data=json.dumps({}),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data['error'], 'Email is required')

        mock_db_utils.return_value.read_data.assert_not_called()

    @patch('app.db_utils')
    @patch('app.generate_password_hash')
    def test_reset_password_success(self, mock_password_hash, mock_db_utils):
        mock_db = MagicMock()
        mock_db.read_data.return_value = [{'user_id': 1}]
        mock_db.mutate_data.return_value = None
        mock_db_utils.return_value = mock_db

        mock_password_hash.return_value = 'hashed_new_password'

        response = self.client.post(
            '/reset-password',
            data=json.dumps({
                'token': 'valid_reset_token',
                'password': 'new_password'
            }),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'Password reset successful')

        mock_db.read_data.assert_called_once()

        self.assertEqual(mock_db.mutate_data.call_count, 2)

        password_update_call = mock_db.mutate_data.call_args_list[0][0]
        self.assertIn('UPDATE users', password_update_call[0])
        self.assertEqual(password_update_call[1][0], 'hashed_new_password')
        self.assertEqual(password_update_call[1][1], 1)

        token_delete_call = mock_db.mutate_data.call_args_list[1][0]
        self.assertIn('DELETE FROM password_reset_tokens', token_delete_call[0])
        self.assertEqual(token_delete_call[1][0], 'valid_reset_token')

    @patch('app.db_utils')
    def test_reset_password_invalid_token(self, mock_db_utils):
        mock_db = MagicMock()
        mock_db.read_data.return_value = []
        mock_db_utils.return_value = mock_db

        response = self.client.post(
            '/reset-password',
            data=json.dumps({
                'token': 'invalid_token',
                'password': 'new_password'
            }),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data['error'], 'Invalid or expired reset token')

        mock_db.mutate_data.assert_not_called()

    @patch('app.db_utils')
    def test_reset_password_missing_fields(self, mock_db_utils):
        response1 = self.client.post(
            '/reset-password',
            data=json.dumps({'password': 'new_password'}),
            content_type='application/json'
        )

        self.assertEqual(response1.status_code, 400)
        data1 = json.loads(response1.data)
        self.assertEqual(data1['error'], 'Missing required fields')

        response2 = self.client.post(
            '/reset-password',
            data=json.dumps({'token': 'reset_token'}),
            content_type='application/json'
        )

        self.assertEqual(response2.status_code, 400)
        data2 = json.loads(response2.data)
        self.assertEqual(data2['error'], 'Missing required fields')

        mock_db_utils.return_value.read_data.assert_not_called()

if __name__ == '__main__':
    unittest.main()