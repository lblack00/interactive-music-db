# This file was written by Lucas Black
import unittest
from unittest.mock import patch, MagicMock
from flask import Flask
from app import app

class TestUserStats(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    @patch('app.db_utils')
    def test_user_top_genres_success(self, mock_db_utils):
        mock_ratings = [{'item_id': 101}, {'item_id': 102}]
        mock_genres = [{'genre': 'Rock', 'count': 3}, {'genre': 'Jazz', 'count': 1}]
        
        mock_db_instance = MagicMock()
        mock_db_instance.read_data.side_effect = [mock_ratings, mock_genres]
        mock_db_utils.return_value = mock_db_instance

        response = self.app.get('/user-top-genres?user_id=123')

        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(isinstance(data, list))
        self.assertEqual(data[0]['name'], 'Rock')
        self.assertEqual(data[0]['percentage'], 75)

    @patch('app.db_utils')
    def test_user_top_genres_missing_user_id(self, mock_db_utils):
        response = self.app.get('/user-top-genres')
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.get_json())

    @patch('app.db_utils')
    def test_user_top_genres_no_ratings(self, mock_db_utils):
        mock_db_instance = MagicMock()
        mock_db_instance.read_data.return_value = []
        mock_db_utils.return_value = mock_db_instance

        response = self.app.get('/user-top-genres?user_id=456')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), [])

    @patch('app.artist')
    @patch('app.release')
    @patch('app.master')
    def test_get_artist_stats_success(self, mock_master, mock_release, mock_artist):
        artist_id = 789
        discography = [
            {'id': 1, 'title': 'Album1', 'year': 2020},
            {'id': 2, 'title': 'Album2', 'year': 2022}
        ]
        mock_artist.get_artist.return_value = {'id': artist_id, 'name': 'Test Artist'}
        mock_artist.get_discography.return_value = discography

        mock_release.get_all_versions_of_master.side_effect = lambda id: [1, 2, 3] if id == 1 else [4]
        mock_release.get_release_tracklist.side_effect = lambda id: [{'title': 'TrackA'}, {'title': 'TrackB'}]
        mock_master.get_discogs_api_master.return_value = {'images': [{'uri': 'http://image.com/img.jpg'}]}

        response = self.app.get(f'/get-artist-stats?artist_id={artist_id}')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('top_album', data)
        self.assertEqual(data['top_album']['name'], 'Album1')
        self.assertEqual(data['top_track']['name'], 'TrackA')
        self.assertEqual(data['recent_album']['year'], 2022)

    @patch('app.artist')
    def test_get_artist_stats_artist_not_found(self, mock_artist):
        mock_artist.get_artist.return_value = None
        response = self.app.get('/get-artist-stats?artist_id=999')
        self.assertEqual(response.status_code, 404)
        self.assertIn('error', response.get_json())

    @patch('app.artist')
    def test_get_artist_stats_no_discography(self, mock_artist):
        mock_artist.get_artist.return_value = {'id': 999, 'name': 'NoDiscography'}
        mock_artist.get_discography.return_value = []
        response = self.app.get('/get-artist-stats?artist_id=999')
        self.assertEqual(response.status_code, 404)
        self.assertIn('error', response.get_json())

if __name__ == '__main__':
    unittest.main()
