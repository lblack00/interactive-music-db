# This file was written by Jax Hendrickson
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import psycopg
import time
import re
from app import db_utils

class MetacriticScraper:
    def __init__(self):
        self.db = db_utils(dbname='discogs_db', user='postgres')
        self.base_url = "https://www.metacritic.com/browse/albums/release-date/coming-soon/date"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }

    def parse_date(self, date_str):
        """Convert date string to datetime object"""
        try:
            # Convert format like "28 February 2025" to datetime
            return datetime.strptime(date_str, '%d %B %Y').date()
        except ValueError as e:
            print("Error parsing date {}: {}".format(date_str, e))
            return None

    def parse_album_info(self, text):
        """Parse album and any additional info in brackets"""
        # Split by '[' to separate album name and additional info
        parts = text.split('[')
        album = parts[0].strip()
        additional_info = parts[1].rstrip(']').strip() if len(parts) > 1 else None
        return album, additional_info

    def scrape_releases(self):
        try:
            print("Fetching URL:", self.base_url)
            response = requests.get(self.base_url, headers=self.headers)
            print("Response status:", response.status_code)
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find the table containing the releases
            releases = []
            current_date = None
            
            # Look for table rows
            for row in soup.find_all('tr'):
                # Check if this is a date row
                date_match = re.match(r'\d{1,2} \w+ \d{4}', row.text.strip())
                if date_match:
                    current_date = self.parse_date(row.text.strip())
                    print("Found date:", current_date)
                    continue
                
                # If we have columns, this might be a release
                columns = row.find_all('td')
                if current_date and len(columns) >= 2:
                    artist = columns[0].text.strip()
                    album_text = columns[1].text.strip()
                    
                    # Parse album name and additional info
                    album_name, additional_info = self.parse_album_info(album_text)
                    
                    release = {
                        'artist': artist,
                        'title': album_name,
                        'release_date': current_date,
                        'additional_info': additional_info,
                        'source_url': self.base_url
                    }
                    
                    print("Found release:", release)
                    self.save_release(release)
                    releases.append(release)
            
            return releases

        except Exception as e:
            print("Error scraping Metacritic: {}".format(e))
            return []

    def save_release(self, release):
        query = """
            INSERT INTO upcoming_releases 
            (title, artist, release_date, additional_info, source_url)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (title, artist) 
            DO UPDATE SET 
                release_date = EXCLUDED.release_date,
                additional_info = EXCLUDED.additional_info,
                last_updated = CURRENT_TIMESTAMP;
        """
        
        self.db.mutate_data(query, (
            release['title'],
            release['artist'],
            release['release_date'],
            release['additional_info'],
            release['source_url']
        ))

    def run(self):
        while True:
            print("Starting Metacritic scrape...")
            releases = self.scrape_releases()
            print("Scraped {} releases".format(len(releases)))
            
            # Sleep for 6 hours before next scrape
            print("Scrape complete. Sleeping for 6 hours...")
            time.sleep(21600)

if __name__ == "__main__":
    scraper = MetacriticScraper()
    scraper.run() 