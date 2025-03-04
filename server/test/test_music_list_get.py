# Test was written by Matthew Stenvold
import unittest
from unittest.mock import patch, MagicMock
from flask import jsonify
import sys
sys.path.insert(0, '..')  # Add parent directory to path
from app import app, get_user_music_list  # Import Flask app


class TestGetUserMusicList(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Set up application context before running tests."""
        cls.app_context = app.app_context()
        cls.app_context.push()

    @classmethod
    def tearDownClass(cls):
        """Tear down application context after all tests."""
        cls.app_context.pop()

    @patch('app.db_utils')  # Mock db_utils
    @patch('app.master')  # Mock master class
    def test_valid_user_with_ratings_master(self, mock_master, mock_db_utils):
        """Test a valid user retrieving master ratings."""
        
        # Mock database connection
        mock_db = MagicMock()
        mock_db_utils.return_value = mock_db

        # Mock user lookup
        mock_db.read_data.side_effect = [
            [{'id': 1}],  # User found
            [{'item_id': 101, 'rating': 9, 'created_at': '2025-03-01'}]  # One rating
        ]
        
        # Mock master lookup
        mock_master.get_master.return_value = [{'title': 'Test Song'}]

        response, status_code = get_user_music_list('testuser', 'master')

        expected_data = [{'id': 101, 'name': 'Test Song', 'rating': 9, 'created_at': '2025-03-01'}]
        
        self.assertEqual(status_code, 200)
        self.assertEqual(response.json, expected_data)

    @patch('app.db_utils')
    @patch('app.artist')  # Mock artist class
    def test_valid_user_with_ratings_artist(self, mock_artist, mock_db_utils):
        """Test a valid user retrieving artist ratings."""

        # Mock database connection
        mock_db = MagicMock()
        mock_db_utils.return_value = mock_db

        # Mock user lookup
        mock_db.read_data.side_effect = [
            [{'id': 1}],  # User found
            [{'item_id': 202, 'rating': 8, 'created_at': '2025-03-02'}]  # One rating for artist
        ]

        # Mock artist lookup
        mock_artist.get_artist.return_value = [{'name': 'Test Artist'}]

        response, status_code = get_user_music_list('testuser', 'artist')

        expected_data = [{'id': 202, 'name': 'Test Artist', 'rating': 8, 'created_at': '2025-03-02'}]

        self.assertEqual(status_code, 200)
        self.assertEqual(response.json, expected_data)

    @patch('app.db_utils')
    @patch('app.track')  # Mock track class
    def test_valid_user_with_ratings_track(self, mock_track, mock_db_utils):
        """Test a valid user retrieving track ratings."""

        # Mock database connection
        mock_db = MagicMock()
        mock_db_utils.return_value = mock_db

        # Mock user lookup
        mock_db.read_data.side_effect = [
            [{'id': 1}],  # User found
            [{'item_id': 202, 'rating': 8, 'created_at': '2025-03-02'}]  # One rating for artist
        ]

        # Mock track lookup
        mock_track.get_track.return_value = [{'name': 'Test track'}]

        response, status_code = get_user_music_list('testuser', 'track')

        expected_data = [{'id': 202, 'name': 'Test track', 'rating': 8, 'created_at': '2025-03-02'}]

        self.assertEqual(status_code, 200)
        self.assertEqual(response.json, expected_data)

    @patch('app.db_utils')
    def test_user_not_found(self, mock_db_utils):
        """Test response when the user is not found."""
        mock_db = MagicMock()
        mock_db_utils.return_value = mock_db

        # Simulate no user found
        mock_db.read_data.return_value = []

        response, status_code = get_user_music_list('unknownuser', 'master')

        self.assertEqual(status_code, 404)
        self.assertEqual(response.json, {'error': 'User not found'})

    @patch('app.db_utils')
    def test_user_no_ratings(self, mock_db_utils):
        """Test response when user has no ratings."""
        mock_db = MagicMock()
        mock_db_utils.return_value = mock_db

        mock_db.read_data.side_effect = [
            [{'id': 1}],  # User found
            []  # No ratings found
        ]

        response, status_code = get_user_music_list('testuser', 'master')

        self.assertEqual(status_code, 200)
        self.assertEqual(response.json, [])

    @patch('app.db_utils')
    def test_invalid_item_type(self, mock_db_utils):
        """Test handling of an invalid item type."""
        mock_db = MagicMock()
        mock_db_utils.return_value = mock_db

        mock_db.read_data.side_effect = [
            [{'id': 1}],  # User found
            [{'item_id': 101, 'rating': 9, 'created_at': '2025-03-01'}]  # One rating
        ]

        response, status_code = get_user_music_list('testuser', 'invalid_type')

        self.assertEqual(status_code, 200)
        self.assertEqual(response.json, [])  # Expect an empty list

if __name__ == '__main__':
    unittest.main()
