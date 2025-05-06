# This file was written by Lucas Black
import unittest
from unittest.mock import patch, MagicMock
from app import app
from artist import artist

class TestArtistIntegrationAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        artist.set_db_for_testing()

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_get_artist_success(self):
        artist_id = 12345

        response = self.app.get(f'/artist?artist_id={artist_id}')
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertIn("payload", data)
        self.assertIn("artist", data["payload"])
        self.assertIsInstance(data["payload"]["artist"], list)
        self.assertGreater(len(data["payload"]["artist"]), 0)
        self.assertEqual(data["payload"]["artist"][0]["name"], "Test Artist")
        self.assertEqual(data["payload"]["artist"][0]["id"], artist_id)

    def test_get_artist_not_found(self):
        artist_id = -1

        response = self.app.get(f'/artist?artist_id={artist_id}')
        data = response.get_json()

        self.assertEqual(response.status_code, 404)
        self.assertIn("error", data)
        self.assertEqual(data["error"], "Artist not found")

    def test_get_artist_invalid_id(self):
        response = self.app.get('/artist?artist_id=abc')
        data = response.get_json()

        self.assertEqual(response.status_code, 400)
        self.assertIn("error", data)
        self.assertEqual(data["error"], "Invalid artist_id format")

    def test_get_artist_missing_id(self):
        response = self.app.get('/artist')
        data = response.get_json()

        self.assertEqual(response.status_code, 400)
        self.assertIn("error", data)
        self.assertEqual(data["error"], "Missing artist_id parameter")

    @patch('app.artist.get_artist')
    def test_get_artist_fail(self, mock_artist):
        artist_id = 12355

        mock_artist.side_effect = Exception()

        response = self.app.get(f'/artist?artist_id={artist_id}')
        data = response.get_json()

        self.assertEqual(response.status_code, 500)
        self.assertIn("error", data)

    @patch('app.artist.get_discography')
    @patch('app.master.get_discogs_api_master')
    def test_get_artist_discography_images_success(self, mock_discogs_api, mock_discography):
        artist_id = 12345
        mock_discography.return_value = [
            {"id": 1001, "title": "Album 1"},
            {"id": 1002, "title": "Album 2"},
            {"id": 1003, "title": "Album 3"}
        ]

        mock_discogs_api.side_effect = [
            {
                'images': [
                    {"uri": "http://discogs.com/album1.jpg", "type": "primary"},
                    {"uri": "http://discogs.com/album1_back.jpg", "type": "secondary"}
                ]
            },
            None,
            {
                'images': [
                    {"uri": "http://discogs.com/album3.jpg", "type": "primary"}
                ]
            }
        ]

        response = self.app.get(f'/artist-discography-images?artist_id={artist_id}')
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertIn("payload", data)
        self.assertIsInstance(data["payload"], dict)
        self.assertEqual(data["payload"]["1001"], "http://discogs.com/album1.jpg")
        self.assertEqual(data["payload"]["1003"], "http://discogs.com/album3.jpg")
        self.assertNotIn("1002", data["payload"])

        mock_discography.assert_called_once_with(artist_id)
        self.assertEqual(mock_discogs_api.call_count, 3)

    @patch('app.artist.get_discography')
    def test_get_artist_discography_images_invalid_id(self, mock_discography):
        response = self.app.get('/artist-discography-images?artist_id=abc')
        self.assertEqual(response.status_code, 400)

        mock_discography.assert_not_called()

    @patch('app.artist.get_discography')
    def test_get_artist_discography_images_missing_id(self, mock_discography):
        response = self.app.get('/artist-discography-images')
        self.assertEqual(response.status_code, 400)

        mock_discography.assert_not_called()

    @patch('app.artist.get_discography')
    def test_get_artist_discography_images_exception(self, mock_discography):
        artist_id = 12348
        mock_discography.side_effect = Exception("Test exception")

        response = self.app.get(f'/artist-discography-images?artist_id={artist_id}')
        self.assertEqual(response.status_code, 500)

        data = response.get_json()
        self.assertIn("error", data)

    def test_get_artist_image_success(self):
        mock_artist = MagicMock()
        mock_artist.images = [{'uri': 'http://example.com/image1.jpg'}, {'uri': 'http://example.com/image2.jpg'}]
        
        mock_client = MagicMock()
        mock_client.artist.return_value = mock_artist
        
        result = artist.get_discogs_api_artist(123, True, mock_client)
        
        mock_client.artist.assert_called_with(123)
        
        self.assertEqual(result, {
            "images": [{'uri': 'http://example.com/image1.jpg'}, {'uri': 'http://example.com/image2.jpg'}]
        })

    def test_get_artist_image_no_images(self):
        mock_artist = MagicMock()
        mock_artist.images = []
        
        mock_client = MagicMock()
        mock_client.artist.return_value = mock_artist
        
        result = artist.get_discogs_api_artist(123, True, mock_client)
        
        self.assertEqual(result, {"images": []})

    def test_get_artist_image_exception(self):
        mock_client = MagicMock()
        mock_client.artist.side_effect = Exception("API Error")
        
        with patch('builtins.print') as mock_print:
            result = artist.get_discogs_api_artist(123, True, mock_client)
            mock_print.assert_called_with("Error retrieving artist: API Error")
            self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()