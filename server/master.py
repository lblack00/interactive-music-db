# This file was written by Lucas Black
from db_utils import db_utils

class master:
    db = db_utils(dbname='discogs_db', user='postgres')

    @staticmethod
    def get_discogs_api_master(master_id, authenticate_discogs_API, discogs_client_instance):
        if not authenticate_discogs_API:
            return None

        if discogs_client_instance is None:
            print("Discogs client not initialized!")
            return None

        try:
            master = discogs_client_instance.master(master_id)
            images = [{'uri': img['uri']} for img in master.images] if master.images else []
            return {"images": images}
        except Exception as e:
            print(f"Error retrieving master: {e}")
            return None

    @staticmethod
    def get_all_master_releases_from_artist(artist_name):
        query = """SELECT * FROM master_artist
                   JOIN master ON master.id=master_artist.master_id
                   WHERE artist_name='%s';"""

        return master.db.read_data(query, (artist_name,))

    @staticmethod
    def get_master(master_id):
        query = "SELECT * FROM master WHERE id=%s;"

        return master.db.read_data(query, (master_id,))

    @staticmethod
    def get_master_artist(master_id):
        query = "SELECT * FROM master_artist WHERE master_id=%s;"

        return master.db.read_data(query, (master_id,))

    @staticmethod
    def get_master_video(master_id):
        query = "SELECT * FROM master_video WHERE master_id=%s;"

        return master.db.read_data(query, (master_id,))

    @staticmethod
    def get_master_genre(master_id):
        query = "SELECT * FROM master_genre WHERE master_id=%s;"

        return master.db.read_data(query, (master_id,))

    @staticmethod
    def get_master_style(master_id):
        query = "SELECT * FROM master_style WHERE master_id=%s;"

        return master.db.read_data(query, (master_id,))

    @staticmethod
    def get_master_release_id(master_id):
        query = "SELECT main_release FROM master WHERE id=%s;"

        return master.db.read_data(query, (master_id,))

    @classmethod
    def set_db_for_testing(cls, dbname='test_discogs_db', user='postgres', 
                         password='postgres', host='localhost', port='5433'):
        cls.db = db_utils(dbname=dbname, user=user, password=password, 
                         host=host, port=port)
        
    @classmethod
    def reset_db(cls):
        cls.db = db_utils(dbname='discogs_db', user='postgres')