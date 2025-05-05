# This file was written by Lucas Black
import unittest
from unittest.mock import patch, MagicMock
from app import app
from master import master

class TestMasterIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        master.set_db_for_testing()
        cls.db = master.db
        cls.test_master_id = 9999999

        cls.db.mutate_data("INSERT INTO master (id, title, main_release) VALUES (%s, %s, %s)",
            (cls.test_master_id, 'Temp Test Master', 12345,))
        cls.db.mutate_data("INSERT INTO master_artist (master_id, artist_id, artist_name) VALUES (%s, %s, %s)",
            (cls.test_master_id, 1, 'Test Artist',))
        cls.db.mutate_data("INSERT INTO master_video (master_id, title, duration) VALUES (%s, %s, %s)",
            (cls.test_master_id, 'Test Video', 120,))
        cls.db.mutate_data("INSERT INTO master_genre (master_id, genre) VALUES (%s, %s)",
            (cls.test_master_id, 'Rock'))
        cls.db.mutate_data("INSERT INTO master_style (master_id, style) VALUES (%s, %s)",
            (cls.test_master_id, 'Psychedelic Rock'))

    @classmethod
    def tearDownClass(cls):
        cls.db.mutate_data("DELETE FROM master_style WHERE master_id = %s", (cls.test_master_id,))
        cls.db.mutate_data("DELETE FROM master_genre WHERE master_id = %s", (cls.test_master_id,))
        cls.db.mutate_data("DELETE FROM master_video WHERE master_id = %s", (cls.test_master_id,))
        cls.db.mutate_data("DELETE FROM master_artist WHERE master_id = %s", (cls.test_master_id,))
        cls.db.mutate_data("DELETE FROM master WHERE id = %s", (cls.test_master_id,))

    def test_get_master(self):
        result = master.get_master(self.test_master_id)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['id'], self.test_master_id)

    def test_get_master_artist(self):
        result = master.get_master_artist(self.test_master_id)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['master_id'], self.test_master_id)
        self.assertEqual(result[0]['artist_name'], 'Test Artist')

    def test_get_master_video(self):
        result = master.get_master_video(self.test_master_id)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['title'], 'Test Video')

    def test_get_master_genre(self):
        result = master.get_master_genre(self.test_master_id)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['genre'], 'Rock')

    def test_get_master_style(self):
        result = master.get_master_style(self.test_master_id)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['style'], 'Psychedelic Rock')

    def test_get_master_release_id(self):
        result = master.get_master_release_id(self.test_master_id)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['main_release'], 12345)

class TestMasterIntegrationAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        master.set_db_for_testing()

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_get_master_not_found(self):
        master_id = -1

        response = self.app.get(f'/master/?master_id={master_id}')
        data = response.get_json()

        self.assertEqual(response.status_code, 404)
        self.assertIn("error", data)
        self.assertEqual(data["error"], "Master not found")

    def test_get_master_invalid_id(self):
        response = self.app.get('/master/?master_id=abc')
        data = response.get_json()

        self.assertEqual(response.status_code, 400)
        self.assertIn("error", data)
        self.assertEqual(data["error"], "Invalid master_id format")

    def test_get_master_missing_id(self):
        response = self.app.get('/master/')
        data = response.get_json()

        self.assertEqual(response.status_code, 400)
        self.assertIn("error", data)
        self.assertEqual(data["error"], "Missing master_id parameter")

    def test_get_master_image_success(self):
        mock_master = MagicMock()
        mock_master.images = [{'uri': 'http://example.com/image1.jpg'}, {'uri': 'http://example.com/image2.jpg'}]
        
        mock_client = MagicMock()
        mock_client.master.return_value = mock_master
        
        result = master.get_discogs_api_master(123, True, mock_client)
        
        mock_client.master.assert_called_with(123)
        
        self.assertEqual(result, {
            "images": [{'uri': 'http://example.com/image1.jpg'}, {'uri': 'http://example.com/image2.jpg'}]
        })

    def test_get_master_image_no_images(self):
        mock_master = MagicMock()
        mock_master.images = []
        
        mock_client = MagicMock()
        mock_client.master.return_value = mock_master
        
        result = master.get_discogs_api_master(123, True, mock_client)
        
        self.assertEqual(result, {"images": []})

    def test_get_master_image_exception(self):
        mock_client = MagicMock()
        mock_client.master.side_effect = Exception("API Error")
        
        with patch('builtins.print') as mock_print:
            result = master.get_discogs_api_master(123, True, mock_client)
            mock_print.assert_called_with("Error retrieving master: API Error")
            self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()
