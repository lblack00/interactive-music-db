# This file was written by Lucas Black
import json
import unittest
from unittest.mock import patch, MagicMock
from flask import Flask, session
from app import app

class TestSpotify(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.client = self.app.test_client()
        self.app.testing = True
        self.app.secret_key = 'test_secret_key'

        self.test_user_id = '67890'
        self.access_token = 'test_access_token'
        self.refresh_token = 'test_refresh_token'
        self.expires_in = 3600

        self.spotify_playlists_response = {
            'items': [
                {
                    'id': 'playlist1',
                    'name': 'My Playlist 1',
                    'description': 'First test playlist',
                    'images': [{'url': 'http://example.com/image1.jpg'}]
                },
                {
                    'id': 'playlist2',
                    'name': 'My Playlist 2',
                    'description': 'Second test playlist',
                    'images': [{'url': 'http://example.com/image2.jpg'}]
                }
            ],
            'total': 2
        }

    def test_save_spotify_tokens_not_authenticated(self):
        with self.client.session_transaction() as sess:
            if 'user' in sess:
                del sess['user']

        response = self.client.post(
            '/update-spotify-tokens',
            json={
                'access_token': self.access_token,
                'refresh_token': self.refresh_token,
                'expires_in': self.expires_in,
                'connected': True
            }
        )

        self.assertEqual(response.status_code, 401)
        data = json.loads(response.data)
        self.assertEqual(data['error'], 'Not authenticated')

    def test_save_spotify_tokens_no_data(self):
        with self.client.session_transaction() as sess:
            sess['user'] = {'id': self.test_user_id, 'username': 'testuser'}

        response = self.client.post('/update-spotify-tokens',
                                     json={},
                                     content_type='application/json')

        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data['error'], 'No data provided')

    def test_save_spotify_tokens_connect(self):
        with self.client.session_transaction() as sess:
            sess['user'] = {'id': self.test_user_id, 'username': 'testuser'}

        response = self.client.post(
            '/update-spotify-tokens',
            json={
                'access_token': self.access_token,
                'refresh_token': self.refresh_token,
                'expires_in': self.expires_in,
                'connected': True
            }
        )

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['success'], 'Save Spotify OAuth tokens')

        with self.client.session_transaction() as sess:
            self.assertTrue('spotify' in sess['user'])
            self.assertEqual(sess['user']['spotify']['access_token'], self.access_token)
            self.assertEqual(sess['user']['spotify']['refresh_token'], self.refresh_token)
            self.assertEqual(sess['user']['spotify']['expires_in'], self.expires_in)
            self.assertTrue(sess['user']['spotify']['connected'])

    def test_save_spotify_tokens_disconnect(self):
        with self.client.session_transaction() as sess:
            sess['user'] = {
                'id': self.test_user_id,
                'username': 'testuser',
                'spotify': {
                    'access_token': self.access_token,
                    'refresh_token': self.refresh_token,
                    'expires_in': self.expires_in,
                    'connected': True
                }
            }

        response = self.client.post(
            '/update-spotify-tokens',
            json={
                'connected': False
            }
        )

        self.assertEqual(response.status_code, 200)

        with self.client.session_transaction() as sess:
            self.assertFalse(sess['user']['spotify']['connected'])
            self.assertEqual(sess['user']['spotify']['access_token'], self.access_token)

    def test_get_spotify_status_connected(self):
        with self.client.session_transaction() as sess:
            sess['user'] = {
                'id': self.test_user_id,
                'username': 'testuser',
                'spotify': {
                    'connected': True
                }
            }

        response = self.client.get('/get-spotify-status')

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['connected'])

    def test_get_spotify_status_disconnected(self):
        with self.client.session_transaction() as sess:
            sess['user'] = {
                'id': self.test_user_id,
                'username': 'testuser',
                'spotify': {
                    'connected': False
                }
            }

        response = self.client.get('/get-spotify-status')

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertFalse(data['connected'])

    def test_get_spotify_status_no_spotify_data(self):
        with self.client.session_transaction() as sess:
            sess['user'] = {
                'id': self.test_user_id,
                'username': 'testuser'
            }

        response = self.client.get('/get-spotify-status')

        self.assertEqual(response.status_code, 204)


    def test_get_spotify_status_not_logged_in(self):
        with self.client.session_transaction() as sess:
            if 'user' in sess:
                del sess['user']

        response = self.client.get('/get-spotify-status')

        self.assertEqual(response.status_code, 204)


    @patch('requests.get')
    def test_get_spotify_playlists_not_authenticated(self, mock_requests_get):
        with self.client.session_transaction() as sess:
            if 'user' in sess:
                del sess['user']

        response = self.client.get('/get-spotify-playlists')

        self.assertEqual(response.status_code, 401)
        data = json.loads(response.data)
        self.assertEqual(data['error'], 'Spotify not connected')

    @patch('requests.get')
    def test_get_spotify_playlists_not_connected(self, mock_requests_get):
        with self.client.session_transaction() as sess:
            sess['user'] = {
                'id': self.test_user_id,
                'username': 'testuser',
                'spotify': {
                    'connected': False
                }
            }

        response = self.client.get('/get-spotify-playlists')

        self.assertEqual(response.status_code, 401)
        data = json.loads(response.data)
        self.assertEqual(data['error'], 'Spotify not connected')

    @patch('requests.get')
    def test_get_spotify_playlists_no_access_token(self, mock_requests_get):
        with self.client.session_transaction() as sess:
            sess['user'] = {
                'id': self.test_user_id,
                'username': 'testuser',
                'spotify': {
                    'connected': True
                }
            }

        response = self.client.get('/get-spotify-playlists')

        self.assertEqual(response.status_code, 401)
        data = json.loads(response.data)
        self.assertEqual(data['error'], 'No access token found')

    @patch('requests.get')
    def test_get_spotify_playlists_success(self, mock_requests_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = self.spotify_playlists_response
        mock_requests_get.return_value = mock_response

        with self.client.session_transaction() as sess:
            sess['user'] = {
                'id': self.test_user_id,
                'username': 'testuser',
                'spotify': {
                    'connected': True,
                    'access_token': self.access_token
                }
            }

        response = self.client.get('/get-spotify-playlists')

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data, self.spotify_playlists_response)

        mock_requests_get.assert_called_once_with(
            'https://api.spotify.com/v1/me/playlists',
            headers={
                'Authorization': f'Bearer {self.access_token}',
                'Content-Type': 'application/json'
            },
            params={'limit': 50}
        )

    @patch('requests.get')
    def test_get_spotify_playlists_token_expired(self, mock_requests_get):
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_response.text = 'The access token expired'
        mock_requests_get.return_value = mock_response

        with self.client.session_transaction() as sess:
            sess['user'] = {
                'id': self.test_user_id,
                'username': 'testuser',
                'spotify': {
                    'connected': True,
                    'access_token': self.access_token
                }
            }

        response = self.client.get('/get-spotify-playlists')

        self.assertEqual(response.status_code, 401)
        data = json.loads(response.data)
        self.assertEqual(data['error'], 'Spotify token expired')

    @patch('requests.get')
    def test_get_spotify_playlists_api_error(self, mock_requests_get):
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.text = 'Internal Server Error'
        mock_requests_get.return_value = mock_response

        with self.client.session_transaction() as sess:
            sess['user'] = {
                'id': self.test_user_id,
                'username': 'testuser',
                'spotify': {
                    'connected': True,
                    'access_token': self.access_token
                }
            }

        response = self.client.get('/get-spotify-playlists')

        self.assertEqual(response.status_code, 500)
        data = json.loads(response.data)
        self.assertEqual(data['error'], 'Spotify API error: Internal Server Error')

    @patch('requests.get')
    def test_get_spotify_playlists_exception(self, mock_requests_get):
        mock_requests_get.side_effect = Exception("Connection error")

        with self.client.session_transaction() as sess:
            sess['user'] = {
                'id': self.test_user_id,
                'username': 'testuser',
                'spotify': {
                    'connected': True,
                    'access_token': self.access_token
                }
            }

        response = self.client.get('/get-spotify-playlists')

        self.assertEqual(response.status_code, 500)
        data = json.loads(response.data)
        self.assertEqual(data['error'], 'Error fetching playlists: Connection error')

if __name__ == '__main__':
    unittest.main()