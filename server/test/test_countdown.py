#this file was written by jax hendrickson
import unittest
from datetime import datetime, timedelta
from app import app
import json

class TestCountdown(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_upcoming_releases_endpoint(self):
        """Test that the upcoming-releases endpoint returns correct format"""
        response = self.app.get('/upcoming-releases')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('releases', data)
        self.assertTrue(isinstance(data['releases'], list))

    def test_release_data_structure(self):
        """Test that each release has the required fields"""
        response = self.app.get('/upcoming-releases')
        data = json.loads(response.data)
        
        if data['releases']:  # If there are any releases
            release = data['releases'][0]
            required_fields = ['title', 'artist', 'release_date']
            for field in required_fields:
                self.assertIn(field, release)

    def test_release_dates_are_future(self):
        """Test that all release dates are in the future"""
        response = self.app.get('/upcoming-releases')
        data = json.loads(response.data)
        today = datetime.now().date()
        
        for release in data['releases']:
            # Parse the date format 'Fri, 28 Feb 2025 00:00:00 GMT'
            release_date = datetime.strptime(
                release['release_date'], 
                '%a, %d %b %Y %H:%M:%S GMT'
            ).date()
            self.assertGreaterEqual(release_date, today)

    def test_releases_are_ordered(self):
        """Test that releases are ordered by date"""
        response = self.app.get('/upcoming-releases')
        data = json.loads(response.data)
        
        if len(data['releases']) > 1:
            dates = [
                datetime.strptime(
                    r['release_date'], 
                    '%a, %d %b %Y %H:%M:%S GMT'
                ).date() 
                for r in data['releases']
            ]
            self.assertEqual(dates, sorted(dates))

    def test_valid_release_dates(self):
        """Test that all release dates can be parsed"""
        response = self.app.get('/upcoming-releases')
        data = json.loads(response.data)
        
        for release in data['releases']:
            try:
                release_date = datetime.strptime(
                    release['release_date'], 
                    '%a, %d %b %Y %H:%M:%S GMT'
                )
                self.assertIsInstance(release_date, datetime)
            except ValueError as e:
                self.fail(f"Invalid date format for {release['title']}: {release['release_date']}")

if __name__ == '__main__':
    unittest.main() 