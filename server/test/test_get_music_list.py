# This file was written by Lucas Black
import unittest
import json
from unittest import mock
from flask import Flask
from app import app
from datetime import datetime

class TestGetMusicList(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

        self.user = "testuser"
        self.user_id = 123
        self.date1 = datetime(2023, 5, 1)
        self.date2 = datetime(2023, 4, 15)

    @mock.patch('app.db_utils')
    @mock.patch('app.master')
    def test_get_user_music_list_master_success(self, mock_master, mock_db_utils):
        mock_db = mock_db_utils.return_value

        mock_db.read_data.side_effect = [
            [{'id': self.user_id}],
            [
                {'item_id': '101', 'rating': 5, 'created_at': self.date1},
                {'item_id': '102', 'rating': 4, 'created_at': self.date2}
            ]
        ]

        mock_master.get_master.side_effect = lambda item_id: [{'title': f'Test Album {item_id}', 'id': item_id}]

        response = self.app.get(f'/api/musiclist/{self.user}/master')

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['id'], '101')
        self.assertEqual(data[0]['name'], 'Test Album 101')
        self.assertEqual(data[0]['rating'], 5)
        self.assertEqual(data[1]['id'], '102')
        self.assertEqual(data[1]['name'], 'Test Album 102')
        self.assertEqual(data[1]['rating'], 4)

        mock_db.read_data.assert_has_calls([
            mock.call("SELECT id FROM users WHERE username = %s;", (self.user,)),
            mock.call("""
            SELECT item_id, rating, created_at
            FROM ratings
            WHERE user_id = %s AND item_type = %s
            ORDER BY created_at DESC;
        """, (self.user_id, 'master'))
        ])

        mock_master.get_master.assert_any_call('101')
        mock_master.get_master.assert_any_call('102')

    @mock.patch('app.db_utils')
    @mock.patch('app.artist')
    def test_get_user_music_list_artist_success(self, mock_artist, mock_db_utils):
        mock_db = mock_db_utils.return_value

        mock_db.read_data.side_effect = [
            [{'id': self.user_id}],
            [
                {'item_id': '201', 'rating': 5, 'created_at': self.date1},
                {'item_id': '202', 'rating': 3, 'created_at': self.date2}
            ]
        ]

        mock_artist.get_artist.side_effect = lambda item_id: [{'name': f'Test Artist {item_id}', 'id': item_id}]

        response = self.app.get(f'/api/musiclist/{self.user}/artist')

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['id'], '201')
        self.assertEqual(data[0]['name'], 'Test Artist 201')
        self.assertEqual(data[0]['rating'], 5)
        self.assertEqual(data[1]['id'], '202')
        self.assertEqual(data[1]['name'], 'Test Artist 202')
        self.assertEqual(data[1]['rating'], 3)

        mock_artist.get_artist.assert_any_call('201')
        mock_artist.get_artist.assert_any_call('202')

    @mock.patch('app.db_utils')
    def test_get_user_music_list_user_not_found(self, mock_db_utils):
        mock_db = mock_db_utils.return_value
        mock_db.read_data.return_value = []

        response = self.app.get(f'/api/musiclist/nonexistent_user/master')

        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertEqual(data['error'], 'User not found')

    @mock.patch('app.db_utils')
    def test_get_user_music_list_no_ratings(self, mock_db_utils):
        mock_db = mock_db_utils.return_value
        mock_db.read_data.side_effect = [
            [{'id': self.user_id}],
            []
        ]

        response = self.app.get(f'/api/musiclist/{self.user}/master')

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data, [])

    @mock.patch('app.db_utils')
    @mock.patch('app.master')
    def test_get_user_music_list_missing_item_info(self, mock_master, mock_db_utils):
        mock_db = mock_db_utils.return_value
        mock_db.read_data.side_effect = [
            [{'id': self.user_id}],
            [{'item_id': '101', 'rating': 5, 'created_at': self.date1}]
        ]

        mock_master.get_master.return_value = None

        response = self.app.get(f'/api/musiclist/{self.user}/master')

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data, [])

    @mock.patch('app.db_utils')
    @mock.patch('app.master')
    def test_get_user_music_list_missing_name(self, mock_master, mock_db_utils):
        mock_db = mock_db_utils.return_value
        mock_db.read_data.side_effect = [
            [{'id': self.user_id}],
            [{'item_id': '101', 'rating': 5, 'created_at': self.date1}]
        ]

        mock_master.get_master.return_value = [{'id': '101'}]

        response = self.app.get(f'/api/musiclist/{self.user}/master')

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['name'], 'Unknown')

    @mock.patch('app.db_utils')
    @mock.patch('app.master')
    def test_get_user_music_list_item_info_exception(self, mock_master, mock_db_utils):
        mock_db = mock_db_utils.return_value
        mock_db.read_data.side_effect = [
            [{'id': self.user_id}],
            [{'item_id': '401', 'rating': 5, 'created_at': self.date1}]
        ]

        mock_master.get_master.side_effect = Exception("API failure")

        response = self.app.get(f'/api/musiclist/{self.user}/master')

        self.assertEqual(response.status_code, 500)
        data = json.loads(response.data)
        self.assertEqual(data['error'], 'Server error')

        mock_master.get_master.assert_called_once_with('401')

    @mock.patch('app.db_utils')
    def test_get_user_music_list_database_error(self, mock_db_utils):
        mock_db = mock_db_utils.return_value
        mock_db.read_data.side_effect = Exception("Database connection failed")

        response = self.app.get(f'/api/musiclist/{self.user}/master')

        self.assertEqual(response.status_code, 500)
        data = json.loads(response.data)
        self.assertEqual(data['error'], 'Server error')

if __name__ == '__main__':
    unittest.main()
