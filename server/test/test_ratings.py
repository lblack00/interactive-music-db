# This file was written by Lucas Black
import json
import unittest
from unittest.mock import patch, MagicMock
from flask import Flask, session
from app import app

class TestRatingsAndUserRatingsAPI(unittest.TestCase):
    def setUp(self):
        self.app_context = app.app_context()
        self.app_context.push()
        self.client = app.test_client()
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'secret_key'
        
        self.test_item_type = 'release'
        self.test_item_id = '555'
        self.test_user_id = 'user_123'

    def tearDown(self):
         with self.client.session_transaction() as sess:
             sess.clear()
         self.app_context.pop()

    @patch('app.db_utils')
    def test_get_ratings_ok(self, mock_db_utils):
        mock_db_conn = MagicMock()
        mock_db_utils.return_value = mock_db_conn
        mock_db_conn.read_data.return_value = [{'average': 3.5, 'total': 20}]
        
        response = self.client.get(f'/ratings?item_type={self.test_item_type}&item_id={self.test_item_id}')
        
        self.assertEqual(response.status_code, 200)
        resp_data = json.loads(response.data)
        self.assertEqual(resp_data['average'], 3.5)
        self.assertEqual(resp_data['total'], 20)
        
        mock_db_conn.read_data.assert_called_once()
        call_args, call_kwargs = mock_db_conn.read_data.call_args
        self.assertEqual(call_args[1], (self.test_item_type, self.test_item_id))

    @patch('app.db_utils')
    def test_get_ratings_nothing_found(self, mock_db_utils):
        mock_db_conn = MagicMock()
        mock_db_utils.return_value = mock_db_conn
        mock_db_conn.read_data.return_value = [{'average': None, 'total': 0}]
        
        response = self.client.get(f'/ratings?item_type={self.test_item_type}&item_id={self.test_item_id}')
        
        self.assertEqual(response.status_code, 200)
        resp_data = json.loads(response.data)
        self.assertEqual(resp_data['average'], 0) 
        self.assertEqual(resp_data['total'], 0)

    @patch('app.db_utils')
    def test_get_ratings_db_fails(self, mock_db_utils):
        mock_db_conn = MagicMock()
        mock_db_utils.return_value = mock_db_conn
        mock_db_conn.read_data.side_effect = Exception("DB went boom")
        
        response = self.client.get(f'/ratings?item_type={self.test_item_type}&item_id={self.test_item_id}')
        
        self.assertEqual(response.status_code, 500)
        resp_data = json.loads(response.data)
        # Check error message matches what the endpoint returns
        self.assertEqual(resp_data['error'], 'Server error')

    @patch('app.db_utils')
    def test_get_user_rating_needs_login(self, mock_db_utils):
        # No session setup here
        response = self.client.get(f'/user-rating?item_type={self.test_item_type}&item_id={self.test_item_id}')
        
        self.assertEqual(response.status_code, 401)
        resp_data = json.loads(response.data)
        self.assertEqual(resp_data['error'], 'Not logged in')
        
        mock_db_utils.assert_not_called()

    @patch('app.db_utils')
    def test_get_user_rating_ok(self, mock_db_utils):
        mock_db_conn = MagicMock()
        mock_db_utils.return_value = mock_db_conn
        mock_db_conn.read_data.return_value = [{'rating': 5}]
        
        with self.client.session_transaction() as http_session:
            http_session['user'] = {'id': self.test_user_id, 'username': 'test_student'}
        
        response = self.client.get(f'/user-rating?item_type={self.test_item_type}&item_id={self.test_item_id}')
        
        self.assertEqual(response.status_code, 200)
        resp_data = json.loads(response.data)
        self.assertEqual(resp_data['rating'], 5)
        
        mock_db_conn.read_data.assert_called_once()
        call_args, call_kwargs = mock_db_conn.read_data.call_args
        self.assertEqual(call_args[1], (self.test_user_id, self.test_item_type, self.test_item_id))

    @patch('app.db_utils')
    def test_get_user_rating_nothing_found(self, mock_db_utils):
        mock_db_conn = MagicMock()
        mock_db_utils.return_value = mock_db_conn
        mock_db_conn.read_data.return_value = []
        
        with self.client.session_transaction() as http_session:
            http_session['user'] = {'id': self.test_user_id, 'username': 'test_student'}
        
        response = self.client.get(f'/user-rating?item_type={self.test_item_type}&item_id={self.test_item_id}')
        
        self.assertEqual(response.status_code, 200)
        resp_data = json.loads(response.data)
        self.assertEqual(resp_data['rating'], 0)

    @patch('app.db_utils')
    def test_get_user_rating_db_fails(self, mock_db_utils):
        mock_db_conn = MagicMock()
        mock_db_utils.return_value = mock_db_conn
        mock_db_conn.read_data.side_effect = Exception("DB went boom")
        
        with self.client.session_transaction() as http_session:
            http_session['user'] = {'id': self.test_user_id, 'username': 'test_student'}

        response = self.client.get(f'/user-rating?item_type={self.test_item_type}&item_id={self.test_item_id}')
        
        self.assertEqual(response.status_code, 500)
        resp_data = json.loads(response.data)
        self.assertEqual(resp_data['error'], 'Server error')


class TestRatingsAPI(unittest.TestCase):

    def setUp(self):
        self.app_context = app.app_context()
        self.app_context.push()
        self.client = app.test_client()
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'test_secret_key_for_session'
        self.test_item_type = 'book'
        self.test_item_id = 'book_987'
        self.test_user_id = 'another_user_456'
        self.test_rating_val = 3

    def tearDown(self):
         with self.client.session_transaction() as sess:
             sess.clear()
         self.app_context.pop()

    @patch('app.db_utils')
    def test_get_generic_rating_ok(self, mock_db_utils):
        mock_db_conn = MagicMock()
        mock_db_utils.return_value = mock_db_conn
        mock_db_conn.read_data.return_value = [{'rating': self.test_rating_val}]
        
        req_url = f'/generic-user-rating?item_type={self.test_item_type}&item_id={self.test_item_id}&user_id={self.test_user_id}'
        response = self.client.get(req_url)
        
        self.assertEqual(response.status_code, 200)
        resp_data = json.loads(response.data)
        self.assertEqual(resp_data['rating'], self.test_rating_val)
        
        mock_db_conn.read_data.assert_called_once()
        call_args, call_kwargs = mock_db_conn.read_data.call_args
        self.assertEqual(call_args[1], (self.test_user_id, self.test_item_type, self.test_item_id))

    @patch('app.db_utils')
    def test_get_generic_rating_nothing_found(self, mock_db_utils):
        mock_db_conn = MagicMock()
        mock_db_utils.return_value = mock_db_conn
        mock_db_conn.read_data.return_value = []
        
        req_url = f'/generic-user-rating?item_type={self.test_item_type}&item_id={self.test_item_id}&user_id={self.test_user_id}'
        response = self.client.get(req_url)
        
        self.assertEqual(response.status_code, 200)
        resp_data = json.loads(response.data)
        self.assertEqual(resp_data['rating'], 0)

    def test_get_generic_rating_no_user_id_param(self):
        req_url = f'/generic-user-rating?item_type={self.test_item_type}&item_id={self.test_item_id}'
        response = self.client.get(req_url)
        
        self.assertEqual(response.status_code, 400)
        resp_data = json.loads(response.data)
        self.assertEqual(resp_data['error'], 'Missing user_id')

    @patch('app.db_utils')
    def test_get_generic_rating_db_fails(self, mock_db_utils):
        mock_db_conn = MagicMock()
        mock_db_utils.return_value = mock_db_conn
        mock_db_conn.read_data.side_effect = Exception("DB went boom")

        req_url = f'/generic-user-rating?item_type={self.test_item_type}&item_id={self.test_item_id}&user_id={self.test_user_id}'
        response = self.client.get(req_url)
        
        self.assertEqual(response.status_code, 500)
        resp_data = json.loads(response.data)
        self.assertEqual(resp_data['error'], 'Server error')

    @patch('app.db_utils')
    def test_rate_item_needs_login(self, mock_db_utils):
        # No session setup
        payload = {
            'item_type': self.test_item_type,
            'item_id': self.test_item_id,
            'rating': self.test_rating_val
        }
        response = self.client.post('/rate', json=payload)
        
        self.assertEqual(response.status_code, 401)
        resp_data = json.loads(response.data)
        self.assertEqual(resp_data['error'], 'Not logged in')
        
        mock_db_utils.assert_not_called()

    @patch('app.db_utils')
    def test_rate_item_updates_rating(self, mock_db_utils):
        mock_db_conn = MagicMock()
        mock_db_utils.return_value = mock_db_conn
        mock_db_conn.mutate_data.return_value = [{'id': 50}]
        
        with self.client.session_transaction() as http_session:
            http_session['user'] = {'id': self.test_user_id, 'username': 'another_student'}
        
        payload = {
            'item_type': self.test_item_type,
            'item_id': self.test_item_id,
            'rating': self.test_rating_val
        }
        response = self.client.post('/rate', json=payload)
        
        self.assertEqual(response.status_code, 200)
        resp_data = json.loads(response.data)
        self.assertEqual(resp_data['success'], True)
        
        mock_db_conn.mutate_data.assert_called_once()
        call_args, call_kwargs = mock_db_conn.mutate_data.call_args
        self.assertEqual(call_args[1], (self.test_rating_val, self.test_user_id, self.test_item_type, self.test_item_id)) 

    @patch('app.db_utils')
    def test_rate_item_inserts_new_rating(self, mock_db_utils):
        mock_db_conn = MagicMock()
        mock_db_utils.return_value = mock_db_conn
        mock_db_conn.mutate_data.side_effect = [[], [{'id': 51}]]
        
        with self.client.session_transaction() as http_session:
            http_session['user'] = {'id': self.test_user_id, 'username': 'another_student'}

        payload = {
            'item_type': self.test_item_type,
            'item_id': self.test_item_id,
            'rating': self.test_rating_val
        }
        response = self.client.post('/rate', json=payload)
        
        self.assertEqual(response.status_code, 200)
        resp_data = json.loads(response.data)
        self.assertEqual(resp_data['success'], True)
        self.assertEqual(mock_db_conn.mutate_data.call_count, 2) 
        
        call_args, call_kwargs = mock_db_conn.mutate_data.call_args
        self.assertEqual(call_args[1], (self.test_user_id, \
                                        self.test_item_type, \
                                        self.test_item_id, \
                                        self.test_rating_val))

    @patch('app.db_utils')
    def test_rate_item_db_fails(self, mock_db_utils):
        mock_db_conn = MagicMock()
        mock_db_utils.return_value = mock_db_conn
        mock_db_conn.mutate_data.side_effect = Exception("DB went boom")

        with self.client.session_transaction() as http_session:
            http_session['user'] = {'id': self.test_user_id, 'username': 'another_student'}

        payload = {
            'item_type': self.test_item_type,
            'item_id': self.test_item_id,
            'rating': self.test_rating_val
        }
        response = self.client.post('/rate', json=payload)
        
        self.assertEqual(response.status_code, 500)
        resp_data = json.loads(response.data)
        self.assertEqual(resp_data['error'], 'Server error')

    def test_rate_item_bad_payload(self):
        with self.client.session_transaction() as http_session:
            http_session['user'] = {'id': self.test_user_id, 'username': 'another_student'}
        
        bad_payloads = [
            {'item_id': self.test_item_id, 'rating': self.test_rating_val}, # missing type
            {'item_type': self.test_item_type, 'rating': self.test_rating_val}, # missing id
            {'item_type': self.test_item_type, 'item_id': self.test_item_id}, # missing rating
            {} # empty
        ]
        
        for payload in bad_payloads:
            response = self.client.post('/rate', json=payload)
            self.assertEqual(response.status_code, 500, f"Failed for payload: {payload}")

if __name__ == '__main__':
    unittest.main()