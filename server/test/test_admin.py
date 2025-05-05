# This file was written by Lucas Black
import unittest
from unittest.mock import patch, MagicMock
from flask import session, json
from werkzeug.exceptions import BadRequest
from app import app

from functools import wraps

class TestAdminAPI(unittest.TestCase):
    def setUp(self):
        self.app_context = app.app_context()
        self.app_context.push()
        self.client = app.test_client()
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SECRET_KEY'] = 'test_secret_key'

        self.db_patcher = patch('app.db_utils')
        self.mock_db = self.db_patcher.start()

        self.patcher_is_admin = patch('app.users.is_user_admin')
        self.mock_is_user_admin = self.patcher_is_admin.start()

        self.patcher_get_reports = patch('app.forum.get_reports')
        self.mock_get_reports = self.patcher_get_reports.start()

        self.patcher_resolve_report = patch('app.forum.resolve_report')
        self.mock_resolve_report = self.patcher_resolve_report.start()
        
        self.patcher_delete_reply = patch('app.forum.delete_report_reply')
        self.mock_delete_reply = self.patcher_delete_reply.start()

        self.patcher_delete_thread = patch('app.forum.delete_report_thread')
        self.mock_delete_thread = self.patcher_delete_thread.start()


    def tearDown(self):
        self.db_patcher.stop()
        self.patcher_is_admin.stop()
        self.patcher_get_reports.stop()
        self.patcher_resolve_report.stop()
        self.patcher_delete_reply.stop()
        self.patcher_delete_thread.stop()
        with self.client.session_transaction() as sess:
            sess.clear()
        self.app_context.pop()

    def login_admin(self):
        with self.client.session_transaction() as sess:
            sess['user'] = {'username': 'admin_user', 'id': 1}
        self.mock_is_user_admin.return_value = True

    def login_non_admin(self):
        with self.client.session_transaction() as sess:
            sess['user'] = {'username': 'regular_user', 'id': 2}
        self.mock_is_user_admin.return_value = False

    def test_admin_routes_no_user(self):
        admin_routes = [
            ('/admin/reports', 'GET'),
            ('/admin/reports/resolve/1', 'PUT'),
            ('/admin/reports/delete-reply/1', 'PUT'),
            ('/admin/reports/delete-thread/1', 'PUT')
        ]
        
        for route, method in admin_routes:
            if method == 'GET':
                response = self.client.get(route)
            elif method == 'PUT':
                response = self.client.put(route, json={})
            else:
                continue
                
            self.assertEqual(response.status_code, 403, f"Route: {route}")
            data = response.get_json()
            self.assertIn('error', data)
            self.assertEqual(data['error'], 'Admin access required')

    def test_admin_routes_non_admin_user(self):
        self.login_non_admin()
        
        admin_routes = [
            ('/admin/reports', 'GET'),
            ('/admin/reports/resolve/1', 'PUT'),
            ('/admin/reports/delete-reply/1', 'PUT'),
            ('/admin/reports/delete-thread/1', 'PUT')
        ]
        
        for route, method in admin_routes:
            if method == 'GET':
                response = self.client.get(route)
            elif method == 'PUT':
                 payload = {}
                 if 'resolve' in route:
                     payload = {'isResolved': True}
                 elif 'delete' in route:
                     payload = {'isDeleted': True}
                 response = self.client.put(route, json=payload)
            else: 
                continue
                
            self.assertEqual(response.status_code, 403, f"Route: {route}")
            data = response.get_json()
            self.assertIn('error', data)
            self.assertEqual(data['error'], 'Admin access required')

    def test_get_reports_admin_success(self):
        self.login_admin()
        
        fake_reports = [
            {'id': 1, 'reason': 'Spam', 'reporter': 'user1', 'timestamp': '2023-01-01T12:00:00'},
            {'id': 2, 'reason': 'Abuse', 'reporter': 'user2', 'timestamp': '2023-01-02T12:00:00'}
        ]
        self.mock_get_reports.return_value = fake_reports
        
        response = self.client.get('/admin/reports')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data, fake_reports)
        self.mock_get_reports.assert_called_once()

    def test_get_reports_admin_empty(self):
        self.login_admin()
        self.mock_get_reports.return_value = []
        
        response = self.client.get('/admin/reports')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data, [])
        self.mock_get_reports.assert_called_once()

    def test_get_reports_admin_db_error_returns_none(self):
        self.login_admin()
        self.mock_get_reports.return_value = None
        
        response = self.client.get('/admin/reports')
        self.assertEqual(response.status_code, 500)
        data = response.get_json()
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Database error fetching reports')
        self.mock_get_reports.assert_called_once()

    def test_get_reports_admin_db_exception(self):
        self.login_admin()
        db_error_msg = "Connection failed"
        self.mock_get_reports.side_effect = Exception(db_error_msg)
        
        response = self.client.get('/admin/reports')
        self.assertEqual(response.status_code, 500)
        data = response.get_json()
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Internal server error')
        self.assertIn('message', data)
        self.assertEqual(data['message'], db_error_msg)
        self.mock_get_reports.assert_called_once()

    def test_resolve_report_admin_success(self):
        self.login_admin()
        report_id = 5
        
        for resolve_status in [True, False]:
            payload = {'isResolved': resolve_status}
            response = self.client.put(f'/admin/reports/resolve/{report_id}', json=payload)
            
            self.assertEqual(response.status_code, 200)
            data = response.get_json()
            self.assertIn('success', data)
            self.mock_resolve_report.assert_called_with(report_id, resolve_status)

    def test_resolve_report_admin_bad_request_data(self):
        self.login_admin()
        report_id = 5

        payload = {'wrongKey': True} 
        response = self.client.put(f'/admin/reports/resolve/{report_id}', json=payload)

        self.assertEqual(response.status_code, 500) 
        data = response.get_json()
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Database error resolving report') 
        self.mock_resolve_report.assert_not_called()

    def test_resolve_report_admin_db_exception(self):
        self.login_admin()
        report_id = 5
        db_error_msg = "Failed to update"
        self.mock_resolve_report.side_effect = Exception(db_error_msg)

        payload = {'isResolved': True}
        response = self.client.put(f'/admin/reports/resolve/{report_id}', json=payload)

        self.assertEqual(response.status_code, 500)
        data = response.get_json()
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Internal server error')
        self.assertIn('message', data)
        self.assertEqual(data['message'], db_error_msg)
        self.mock_resolve_report.assert_called_once_with(report_id, True)

    def test_delete_reply_admin_success(self):
        self.login_admin()
        reply_id = 2
        
        for delete_status in [True, False]:
            payload = {'isDeleted': delete_status}
            response = self.client.put(f'/admin/reports/delete-reply/{reply_id}', json=payload)
            
            self.assertEqual(response.status_code, 200)
            data = response.get_json()
            self.assertIn('success', data)
            self.mock_delete_reply.assert_called_with(reply_id, delete_status)

    def test_delete_reply_admin_bad_request_data(self):
        self.login_admin()
        reply_id = 2

        payload = {}
        response = self.client.put(f'/admin/reports/delete-reply/{reply_id}', json=payload)
        
        self.assertEqual(response.status_code, 500)
        data = response.get_json()
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Database error deleting reply')
        self.mock_delete_reply.assert_not_called()

    def test_delete_reply_admin_db_exception(self):
        self.login_admin()
        reply_id = 2
        db_error_msg = "Timeout deleting"
        self.mock_delete_reply.side_effect = Exception(db_error_msg)
        
        payload = {'isDeleted': True}
        response = self.client.put(f'/admin/reports/delete-reply/{reply_id}', json=payload)

        self.assertEqual(response.status_code, 500)
        data = response.get_json()
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Internal server error')
        self.assertIn('message', data)
        self.assertEqual(data['message'], db_error_msg)
        self.mock_delete_reply.assert_called_once_with(reply_id, True)

    def test_delete_thread_admin_success(self):
        self.login_admin()
        thread_id = 3
        
        for delete_status in [True, False]:
            payload = {'isDeleted': delete_status}
            response = self.client.put(f'/admin/reports/delete-thread/{thread_id}', json=payload)
            
            self.assertEqual(response.status_code, 200)
            data = response.get_json()
            self.assertIn('success', data)
            self.mock_delete_thread.assert_called_with(thread_id, delete_status)

    def test_delete_thread_admin_bad_request_data(self):
        self.login_admin()
        thread_id = 3
        
        payload = {'badData': False}
        response = self.client.put(f'/admin/reports/delete-thread/{thread_id}', json=payload)
        
        self.assertEqual(response.status_code, 500)
        data = response.get_json()
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Database error deleting thread')
        self.mock_delete_thread.assert_not_called()

    def test_delete_thread_admin_db_exception(self):
        self.login_admin()
        thread_id = 3
        db_error_msg = "Constraint violation"
        self.mock_delete_thread.side_effect = Exception(db_error_msg)

        payload = {'isDeleted': True}
        response = self.client.put(f'/admin/reports/delete-thread/{thread_id}', json=payload)
        
        self.assertEqual(response.status_code, 500)
        data = response.get_json()
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Internal server error')
        self.assertIn('message', data)
        self.assertEqual(data['message'], db_error_msg)
        self.mock_delete_thread.assert_called_once_with(thread_id, True)

    def test_admin_routes_non_int_ids(self):
        self.login_admin()
        
        bad_routes = [
            '/admin/reports/resolve/abc',
            '/admin/reports/delete-reply/xyz',
            '/admin/reports/delete-thread/not-an-id'
        ]
        
        for route in bad_routes:
            payload = {'isDeleted': True}
            response = self.client.put(route, json=payload)
            self.assertEqual(response.status_code, 404, f"Route: {route}")

if __name__ == '__main__':
    unittest.main()