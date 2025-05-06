# This file was written by Lucas Black
from db_utils import db_utils

class artist:
    db = db_utils(dbname='discogs_db', user='postgres')

    @staticmethod
    def get_discogs_api_artist(artist_id, authenticate_discogs_API, discogs_client_instance):
        if not authenticate_discogs_API:
            return None

        if discogs_client_instance is None:
            print("Discogs client not initialized!")
            return None

        try:
            artist = discogs_client_instance.artist(artist_id)
            images = [{'uri': img['uri']} for img in artist.images] if artist.images else []
            return {"images": images}
        except Exception as e:
            print(f"Error retrieving artist: {e}")
            return None

    @staticmethod
    def get_artist(artist_id):
        query = """
        SELECT a.* 
        FROM artist a
        WHERE a.id = %s;
        """

        # I changed this quere so that it would work and no other function seemed to use this. I put the
        # previous query down below. AFAICT artist_image has basically nothing there - Matthew Stenvold
        #
        #    SELECT a.*, ai.uri as image_uri 
        #    FROM artist a
        #    LEFT JOIN artist_image ai ON a.id = ai.artist_id
        #    WHERE a.id=%s;
        

        return artist.db.read_data(query, (artist_id))

    @staticmethod
    def get_discography(artist_id):
        query = """SELECT * FROM master_artist
                   JOIN master ON master.id=master_artist.master_id
                   WHERE artist_id=%s LIMIT 20;"""

        return artist.db.read_data(query, (artist_id))

    @classmethod
    def set_db_for_testing(cls, dbname='test_discogs_db', user='postgres', 
                         password='postgres', host='localhost', port='5433'):
        cls.db = db_utils(dbname=dbname, user=user, password=password, 
                         host=host, port=port)
        
    @classmethod
    def reset_db(cls):
        cls.db = db_utils(dbname='discogs_db', user='postgres')