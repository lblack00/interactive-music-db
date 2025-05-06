# This file was written by Lucas Black
import os
import json
import unittest
from unittest.mock import patch, MagicMock
from io import BytesIO
from PIL import Image
from flask import session
from app import app, db_utils, get_profile_image_path
from psycopg import errors

class TestUserManagement(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'test-key'
        self.app = app.test_client()
        self.app.testing = True

        with self.app.session_transaction() as sess:
            sess['user'] = {'id': 1, 'username': 'testuser'}

    def tearDown(self):
        pass

    @patch('app.db_utils')
    def test_delete_user_rating(self, mock_db_utils):
        mock_db = MagicMock()
        mock_db_utils.return_value = mock_db
        mock_db.mutate_data.return_value = None

        response = self.app.delete('/delete-user-rating?item_type=master&item_id=123')

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'Rating deleted successfully')

        mock_db.mutate_data.assert_called_once()
        args = mock_db.mutate_data.call_args[0]
        self.assertIn('DELETE FROM ratings', args[0])
        self.assertEqual(args[1][0], 1)
        self.assertEqual(args[1][1], 'master')
        self.assertEqual(args[1][2], '123')

    @patch('app.db_utils')
    def test_delete_user_rating_not_logged_in(self, mock_db_utils):
        client = app.test_client()

        response = client.delete('/delete-user-rating?item_type=master&item_id=123')

        self.assertEqual(response.status_code, 401)
        data = json.loads(response.data)
        self.assertEqual(data['error'], 'Not logged in')

        mock_db_utils.assert_not_called()

    @patch('app.db_utils')
    def test_update_username(self, mock_db_utils):
        mock_db = MagicMock()
        mock_db_utils.return_value = mock_db
        mock_db.mutate_data.return_value = [{'id': 1}]

        response = self.app.post('/update-username',
                                 data=json.dumps({'new_username': 'newusername'}),
                                 content_type='application/json')

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])

        mock_db.mutate_data.assert_called_once()
        args = mock_db.mutate_data.call_args[0]
        self.assertIn('UPDATE users', args[0])
        self.assertEqual(args[1][0], 'newusername')
        self.assertEqual(args[1][1], 1)

    @patch('app.db_utils')
    def test_update_username_already_taken(self, mock_db_utils):
        mock_db = MagicMock()
        mock_db_utils.return_value = mock_db

        mock_db.mutate_data.side_effect = errors.UniqueViolation('Username already taken')

        response = self.app.post('/update-username',
                                 data=json.dumps({'new_username': 'takenname'}),
                                 content_type='application/json')

        self.assertEqual(response.status_code, 409)
        data = json.loads(response.data)
        self.assertEqual(data['error'], 'Username already taken')

    @patch('app.Image')
    @patch('app.os.path.exists')
    @patch('app.os.makedirs')
    def test_update_user_pfp(self, mock_makedirs, mock_path_exists, mock_image):
        mock_path_exists.return_value = False
        mock_img_inst = MagicMock()
        mock_image.open.return_value = mock_img_inst

        test_image = BytesIO()
        Image.new('RGB', (100, 100), color='red').save(test_image, 'PNG')
        test_image.seek(0)

        response = self.app.post('/update-user-pfp',
                                 data={'image': (test_image, 'test.png')},
                                 content_type='multipart/form-data')

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertEqual(data['filename'], '1profilepic.png')

        mock_makedirs.assert_called_once()

    def test_update_user_pfp_invalid_file(self):
        test_file = BytesIO(b'This is not an image')

        response = self.app.post('/update-user-pfp',
                                 data={'image': (test_file, 'test.txt')},
                                 content_type='multipart/form-data')

        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data['error'], 'Invalid file type. Only JPG, JPEG, and PNG are allowed.')

    @patch('app.get_profile_image_path')
    def test_get_profile_image(self, mock_get_path):
        mock_get_path.return_value = '/static/pfp/unknownPFP.png'

        response = self.app.get('/get-profile-image/1')

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['image_url'], '/static/pfp/unknownPFP.png')

        mock_get_path.assert_called_once_with(1)

    @patch('app.db_utils')
    def test_get_bio(self, mock_db_utils):
        mock_db = MagicMock()
        mock_db_utils.return_value = mock_db
        mock_db.read_data.return_value = [{'bio': 'This is a test bio'}]

        response = self.app.get('/get-bio/1')

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['bio'], 'This is a test bio')

        mock_db.read_data.assert_called_once()
        args = mock_db.read_data.call_args[0]
        self.assertIn('SELECT bio FROM users', args[0])
        self.assertEqual(args[1][0], 1)

    @patch('app.db_utils')
    def test_get_bio_user_not_found(self, mock_db_utils):
        mock_db = MagicMock()
        mock_db_utils.return_value = mock_db
        mock_db.read_data.return_value = []

        response = self.app.get('/get-bio/999')

        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertEqual(data['error'], 'User not found')

    @patch('app.db_utils')
    def test_update_bio(self, mock_db_utils):
        mock_db = MagicMock()
        mock_db_utils.return_value = mock_db
        mock_db.mutate_data.return_value = None

        new_bio = "This is my updated bio."
        response = self.app.post('/update-bio',
                                 data=json.dumps({'bio': new_bio}),
                                 content_type='application/json')

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertEqual(data['bio'], new_bio)

        mock_db.mutate_data.assert_called_once()
        args = mock_db.mutate_data.call_args[0]
        self.assertIn('UPDATE users', args[0])
        self.assertEqual(args[1][0], new_bio)
        self.assertEqual(args[1][1], 1)

    @patch('app.db_utils')
    def test_update_bio_too_long(self, mock_db_utils):
        new_bio = "x" * 501
        response = self.app.post('/update-bio',
                                 data=json.dumps({'bio': new_bio}),
                                 content_type='application/json')

        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data['error'], 'Bio cannot be longer than 500 characters')

        mock_db_utils.assert_not_called()

    @patch('app.db_utils')
    def test_get_user_id(self, mock_db_utils):
        mock_db = MagicMock()
        mock_db_utils.return_value = mock_db
        mock_db.read_data.return_value = [{'id': 1}]

        response = self.app.get('/get-user-id/testuser')

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['id'], 1)

        mock_db.read_data.assert_called_once()
        args = mock_db.read_data.call_args[0]
        self.assertIn('SELECT id FROM users', args[0])
        self.assertEqual(args[1][0], 'testuser')

    @patch('app.db_utils')
    def test_get_user_id_not_found(self, mock_db_utils):
        mock_db = MagicMock()
        mock_db_utils.return_value = mock_db
        mock_db.read_data.return_value = []

        response = self.app.get('/get-user-id/nonexistentuser')

        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertEqual(data['error'], 'User not found')

    @patch('app.db_utils')
    def test_user_rating_stats(self, mock_db_utils):
        mock_db = MagicMock()
        mock_db_utils.return_value = mock_db
        mock_db.read_data.return_value = [{'total_ratings': 10, 'average_rating': 4.5}]

        response = self.app.get('/user-rating-stats?user_id=1')

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['total_ratings'], 10)
        self.assertEqual(data['average_rating'], 4.5)

        mock_db.read_data.assert_called_once()
        args = mock_db.read_data.call_args[0]
        self.assertIn('SELECT COUNT(*) AS total_ratings', args[0])
        self.assertEqual(args[1][0], '1')

    @patch('app.db_utils')
    def test_user_rating_stats_missing_user_id(self, mock_db_utils):
        response = self.app.get('/user-rating-stats')

        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data['error'], 'Missing user_id')

        mock_db_utils.assert_not_called()

    @patch('app.master')
    @patch('app.artist')
    @patch('app.db_utils')
    def test_user_recent_activity(self, mock_db_utils, mock_artist, mock_master):
        mock_db = MagicMock()
        mock_db_utils.return_value = mock_db

        mock_activity = [
            {
                'action_type': 'forum_thread',
                'created_at': '2023-05-01 12:00:00',
                'action_id': 1,
                'description': 'Created new thread titled "Test Thread"',
                'relevant_url': '/forum/thread/1'
            },
            {
                'action_type': 'forum_reply',
                'created_at': '2023-05-01 12:30:00',
                'action_id': 2,
                'description': 'Made a reply on the thread "Test Thread"',
                'relevant_url': '/forum/thread/1'
            },
            {
                'action_type': 'rating',
                'created_at': '2023-05-01 13:00:00',
                'action_id': 3,
                'description': 'master 123 5',
                'relevant_url': '/master/123'
            },
            {
                'action_type': 'rating',
                'created_at': '2023-05-01 14:00:00',
                'action_id': 4,
                'description': 'artist 456 4',
                'relevant_url': '/artist/456'
            }
        ]
        mock_db.read_data.return_value = mock_activity

        mock_master.get_master.return_value = [{'title': 'Test Album'}]
        mock_artist.get_artist.return_value = [{'name': 'Test Artist'}]

        response = self.app.get('/user-recent-activity?user_id=1&limit=5')

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 4)

        for item in data:
            if item['action_type'] == 'master_rating':
                self.assertEqual(item['description'], 'Rated "Test Album" 5 stars')
            elif item['action_type'] == 'artist_rating':
                self.assertEqual(item['description'], 'Rated "Test Artist" 4 stars')

        mock_db.read_data.assert_called_once()
        args = mock_db.read_data.call_args[0]
        self.assertIn('FROM forum_threads ft', args[0])
        self.assertEqual(args[1][0], '1')
        self.assertEqual(args[1][3], '5')

if __name__ == '__main__':
    unittest.main()