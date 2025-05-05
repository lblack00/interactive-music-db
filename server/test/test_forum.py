# This file was written by Lucas Black
import unittest
import json
from unittest.mock import patch, MagicMock
from datetime import datetime
from app import app
from forum import forum

class TestForumIntegrationAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        forum.set_db_for_testing()

    def setUp(self):
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

        self.thread_data = {
            'id': 9,
            'title': 'New Test Thread',
            'content': 'This is a new test thread content',
            'category': 'General'
        }
        
        self.reply_data = {
            'content': 'This is a new test reply',
            'parentId': None
        }

        self.report_data = {
            'type': 'thread',
            'itemId': 1,
            'reason': 'Reported content'
        }

    @classmethod
    def tearDownClass(cls):
        forum.db.mutate_data("DELETE FROM forum_replies WHERE content=%s;", ("This is a new test reply"))

    def test_get_all_threads_success(self):
        response = self.client.get('/forum/threads')

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)

        self.assertEqual(len(data), 4)
        self.assertEqual(data[0]['id'], 1)
        self.assertEqual(data[0]['title'], 'Test Thread')
        self.assertEqual(data[0]['category'], 'General')
        self.assertEqual(data[0]['date'], 'April 30, 2025')
        self.assertEqual(data[0]['author']['id'], 1)
        self.assertEqual(data[0]['author']['name'], 'Test User')
        self.assertEqual(data[0]['replies'], 4)

    def test_get_all_threads_success_with_limit_and_offset(self):
        response = self.client.get('/forum/threads?category=General&limit=10&offset=0')

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['id'], 1)
        self.assertEqual(data[0]['title'], 'Test Thread')
        self.assertEqual(data[0]['category'], 'General')
        self.assertEqual(data[0]['date'], 'April 30, 2025')
        self.assertEqual(data[0]['author']['id'], 1)
        self.assertEqual(data[0]['author']['name'], 'Test User')
        self.assertEqual(data[0]['replies'], 4)

    @patch('app.forum.get_all_threads')
    def test_get_all_threads_error(self, mock_get_all_threads):
        mock_get_all_threads.side_effect = Exception("Database error")

        response = self.client.get('/forum/threads')

        self.assertEqual(response.status_code, 500)
        data = json.loads(response.data)
        self.assertIn('error', data)
        self.assertIn('Internal server error', data['error'])

    def test_get_forum_categories_success(self):
        response = self.client.get('/forum/categories')

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 3)
        self.assertIn('General', data)
        self.assertIn('Questions', data)
        self.assertIn('Announcements', data)

    @patch('app.forum.get_categories')
    def test_get_forum_categories_error(self, mock_get_categories):
        mock_get_categories.side_effect = Exception("Database error")

        response = self.client.get('/forum/categories')

        self.assertEqual(response.status_code, 500)
        data = json.loads(response.data)
        self.assertIn('error', data)
        self.assertIn('Internal server error', data['error'])

    def test_create_thread(self):
        with patch('app.session', {'user': {'id': 1, 'username': 'Test User'}}):
            response = self.client.post('/forum/thread',
                                        data=json.dumps(self.thread_data),
                                        content_type='application/json')
            
            self.assertEqual(response.status_code, 201)
            data = json.loads(response.data)
            
            self.assertIsNotNone(data['id'])
            self.assertEqual(data['title'], 'New Test Thread')
            self.assertEqual(data['content'], 'This is a new test thread content')
            self.assertEqual(data['category'], 'General')
            self.assertEqual(data['author']['id'], 1)
            self.assertEqual(data['author']['name'], 'Test User')
            self.assertEqual(data['replies'], 0)
            
            verify_response = self.client.get(f'/forum/thread/{data["id"]}')
            self.assertEqual(verify_response.status_code, 200)
            verify_data = json.loads(verify_response.data)
            self.assertEqual(verify_data['title'], 'New Test Thread')

            # clean up so other tests are not affected
            forum.db.mutate_data("DELETE FROM forum_threads WHERE title=%s;", ('New Test Thread'))

    def test_create_thread_not_logged_in(self):
        with patch('app.session', {}):
            response = self.client.post('/forum/thread',
                                         data=json.dumps({}),
                                         content_type='application/json')

            self.assertEqual(response.status_code, 401)
            data = json.loads(response.data)
            self.assertIn('error', data)
            self.assertIn('Not logged in', data['error'])

    def test_create_thread_missing_fields(self):
        with patch('app.session', {'user': {'id': 1, 'username': 'Test User'}}):
            incomplete_data = {
                'title': 'Test Thread',
                'category': 'General'
            }

            response = self.client.post('/forum/thread',
                                         data=json.dumps(incomplete_data),
                                         content_type='application/json')

            self.assertEqual(response.status_code, 400)
            data = json.loads(response.data)
            self.assertIn('error', data)
            self.assertIn('Missing required fields', data['error'])

    def test_create_thread_title_too_long(self):
        with patch('app.session', {'user': {'id': 1, 'username': 'Test User'}}):
            long_title_data = {
                'title': 'A' * 101,
                'content': 'This is a test thread content',
                'category': 'General'
            }

            response = self.client.post('/forum/thread',
                                         data=json.dumps(long_title_data),
                                         content_type='application/json')

            self.assertEqual(response.status_code, 400)
            data = json.loads(response.data)
            self.assertIn('error', data)
            self.assertIn('Title must be less than 100 characters', data['error'])

    def test_get_forum_thread_success(self):
        response = self.client.get('/forum/thread/1')

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)

        self.assertEqual(data['id'], 1)
        self.assertEqual(data['title'], 'Test Thread')
        self.assertEqual(data['content'], 'This is a test thread content')
        self.assertEqual(data['date'], 'April 30, 2025')
        self.assertEqual(data['isEdited'], False)
        self.assertEqual(data['author']['id'], 1)
        self.assertEqual(data['author']['name'], 'Test User')

        self.assertEqual(len(data['replies']), 4)
        self.assertEqual(data['replies'][0]['id'], 1)
        self.assertEqual(data['replies'][0]['content'], 'This is a reply to the test thread')
        self.assertEqual(data['replies'][0]['date'], 'April 30, 2025')
        self.assertEqual(data['replies'][0]['author']['id'], 2)

    def test_get_forum_thread_not_found(self):
        response = self.client.get('/forum/thread/123')

        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Thread not found')

    def test_delete_thread(self):
        with patch('app.session', {'user': {'id': 1, 'username': 'Test User'}}):
            response = self.client.post('/forum/thread',
                                      data=json.dumps(self.thread_data),
                                      content_type='application/json')
            new_thread_id = json.loads(response.data)['id']
            response = self.client.delete(f'/forum/thread/{new_thread_id}')
            
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertIn('message', data)
            self.assertEqual(data['message'], 'Thread deleted successfully')

            verify_response = self.client.get(f'/forum/thread/{new_thread_id}')
            self.assertEqual(verify_response.status_code, 404)

            forum.db.mutate_data("DELETE FROM forum_threads WHERE title=%s;", ('New Test Thread'))

    @patch('app.forum.get_thread')
    def test_get_forum_thread_error(self, mock_get_thread):
        mock_get_thread.side_effect = Exception("Database error")

        response = self.client.get('/forum/thread/1')

        self.assertEqual(response.status_code, 500)
        data = json.loads(response.data)
        self.assertIn('error', data)
        self.assertIn('Internal server error', data['error'])

    def test_add_thread_reply_success(self):
        with patch('app.session', {'user': {'id': 1, 'username': 'Test User'}}):
            response = self.client.post('/forum/thread/1/reply',
                                         data=json.dumps(self.reply_data),
                                         content_type='application/json')

            self.assertEqual(response.status_code, 201)
            data = json.loads(response.data)
            self.assertEqual(data['content'], 'This is a new test reply')
            self.assertEqual(data['isEdited'], False)
            self.assertEqual(data['parentId'], None)
            self.assertEqual(data['author']['id'], 1)
            self.assertEqual(data['author']['name'], 'Test User')

            # clean up
            forum.db.mutate_data("DELETE FROM forum_replies WHERE content=%s;",
                ('This is a new test reply'))

    def test_add_thread_reply_not_logged_in(self):
        with patch('app.session', {}):
            response = self.client.post('/forum/thread/1/reply',
                                         data=json.dumps(self.reply_data),
                                         content_type='application/json')

            self.assertEqual(response.status_code, 401)
            data = json.loads(response.data)
            self.assertIn('error', data)
            self.assertEqual(data['error'], 'Not logged in')

    def test_add_thread_reply_empty_content(self):
        with patch('app.session', {'user': {'id': 1, 'username': 'Test User'}}):
            empty_content_data = {
                'content': '',
                'parentId': None
            }

            response = self.client.post('/forum/thread/1/reply',
                                         data=json.dumps(empty_content_data),
                                         content_type='application/json')

            self.assertEqual(response.status_code, 400)
            data = json.loads(response.data)
            self.assertIn('error', data)
            self.assertEqual(data['error'], 'Reply content cannot be empty')

    # @patch('app.forum.update_reply')
    def test_update_reply_success(self):
        with patch('app.session', {'user': {'id': 1, 'username': 'Test User'}}):
            updated_content = {'content': 'Updated reply content'}
            response = self.client.put('/forum/reply/5',
                                         data=json.dumps(updated_content),
                                         content_type='application/json')

            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertIn('message', data)
            self.assertEqual(data['message'], 'Reply updated successfully')

    def test_update_reply_empty_content(self):
        with patch('app.session', {'user': {'id': 1, 'username': 'Test User'}}):
            empty_content = {'content': ''}
            response = self.client.put('/forum/reply/5',
                                         data=json.dumps(empty_content),
                                         content_type='application/json')

            self.assertEqual(response.status_code, 400)
            data = json.loads(response.data)
            self.assertIn('error', data)
            self.assertEqual(data['error'], 'Reply content cannot be empty')

    def test_update_reply_unauthorized(self):
        with patch('app.session', {'user': {'id': 5, 'username': 'Test User 5'}}):
            updated_content = {'content': 'Updated reply content'}
            response = self.client.put('/forum/reply/5',
                                         data=json.dumps(updated_content),
                                         content_type='application/json')

            self.assertEqual(response.status_code, 403)
            data = json.loads(response.data)
            self.assertIn('error', data)
            self.assertEqual(data['error'], 'Failed to update reply or not authorized')

    def test_delete_reply_unauthorized(self):
        with patch('app.session', {'user': {'id': 5, 'username': 'Test User 5'}}):
            response = self.client.delete('/forum/reply/5')

            self.assertEqual(response.status_code, 403)
            data = json.loads(response.data)
            self.assertIn('error', data)
            self.assertEqual(data['error'], 'Failed to delete reply or not authorized')

    # @patch('app.forum.update_thread')
    def test_update_thread_success(self):
        with patch('app.session', {'user': {'id': 1, 'username': 'Test User'}}):
            updated_content = {'content': 'Updated thread content'}
            response = self.client.put('/forum/thread/3',
                                         data=json.dumps(updated_content),
                                         content_type='application/json')

            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertIn('message', data)
            self.assertEqual(data['message'], 'Thread updated successfully')

    def test_delete_thread_success(self):
        with patch('app.session', {'user': {'id': 3, 'username': 'Admin User'}}):
            response = self.client.delete('/forum/thread/4')

            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertIn('message', data)
            self.assertEqual(data['message'], 'Thread deleted successfully')

            # reset value
            forum.db.mutate_data("UPDATE forum_threads SET is_deleted=FALSE WHERE id=4;")

    def test_report_forum_item_success(self):
        with patch('app.session', {'user': {'id': 1, 'username': 'Test User'}}):
            response = self.client.post('/forum/report',
                                         data=json.dumps(self.report_data),
                                         content_type='application/json')

            self.assertEqual(response.status_code, 201)
            data = json.loads(response.data)
            self.assertIn('message', data)
            self.assertEqual(data['message'], 'Report submitted successfully')

            forum.db.mutate_data("DELETE FROM forum_reports WHERE reason='Reported content';")

    def test_report_forum_item_missing_fields(self):
        with patch('app.session', {'user': {'id': 1, 'username': 'Test User'}}):
            incomplete_report = {
                'type': 'thread',
                'reason': 'Inappropriate content'
            }

            response = self.client.post('/forum/report',
                                         data=json.dumps(incomplete_report),
                                         content_type='application/json')

            self.assertEqual(response.status_code, 400)
            data = json.loads(response.data)
            self.assertIn('error', data)
            self.assertEqual(data['error'], 'Missing required fields')

    # @patch('app.forum.get_thread')
    # @patch('app.forum.add_reference')
    def test_add_forum_reference_success(self):
        with patch('app.session', {'user': {'id': 1, 'username': 'Test User'}}):
            reference_data = {
                'item_type': 'thread',
                'item_id': 1,
                'reference_type': 'article',
                'reference_id': 64,
                'reference_name': 'A Different Article'
            }

            response = self.client.post('/forum/reference',
                                         data=json.dumps(reference_data),
                                         content_type='application/json')

            self.assertEqual(response.status_code, 201)
            data = json.loads(response.data)
            self.assertTrue(data['success'])

            reference_id = data['reference'][0][0]
            reference = forum.get_reference(reference_id)
            self.assertEqual(reference[0]['name'], 'A Different Article')

            forum.db.mutate_data("DELETE FROM forum_references WHERE name=%s;",
                ('A Different Article',))

    def test_add_forum_reference_not_logged_in(self):
        with patch('app.session', {}):
            reference_data = {
                'item_type': 'thread',
                'item_id': 1,
                'reference_type': 'article',
                'reference_id': 42,
                'reference_name': 'Useful Article'
            }

            response = self.client.post('/forum/reference',
                                         data=json.dumps(reference_data),
                                         content_type='application/json')

            data = json.loads(response.data)
            self.assertIn('error', data)
            self.assertEqual(data['error'], 'Not logged in')

    def test_add_forum_reference_thread_not_found(self):
        with patch('app.session', {'user': {'id': 1, 'username': 'Test User'}}):
            reference_data = {
                'item_type': 'thread',
                'item_id': 999,
                'reference_type': 'article',
                'reference_id': 42,
                'reference_name': 'Useful Article'
            }

            response = self.client.post('/forum/reference',
                                         data=json.dumps(reference_data),
                                         content_type='application/json')

            self.assertEqual(response.status_code, 402)
            data = json.loads(response.data)
            self.assertIn('error', data)
            self.assertEqual(data['error'], 'Not authorized')

if __name__ == '__main__':
    unittest.main()