# This file was written by Lucas Black
from db_utils import db_utils

# Class for building SQL release queries and handing them to database connection
class release:
    db = db_utils(dbname='discogs_db', user='postgres')

    @staticmethod
    def get_discogs_api_release(release_id, authenticate_discogs_API, discogs_client_instance):
        if not authenticate_discogs_API:
            return None

        if discogs_client_instance is None:
            print("Discogs client not initialized!")
            return None

        try:
            release = discogs_client_instance.release(release_id)
            images = [{'uri': img['uri']} for img in release.images] if release.images else []
            return {"images": images}
        except Exception as e:
            print(f"Error retrieving release: {e}")
            return None

    # def get_track_credits(track_id):
    @staticmethod
    def get_all_versions_of_master(master_id):
        query = "SELECT * FROM release WHERE master_id=%s;"

        return release.db.read_data(query, (master_id,))

    @staticmethod
    def get_release(release_id):
        # todo: need to sanitize SQL input from a user
        query = "SELECT * FROM release WHERE id=%s;"

        return release.db.read_data(query, (release_id,))

    @staticmethod
    def get_release_tracklist(release_id):
        # todo: need to sanitize SQL input from a user
        query = "SELECT * FROM release_track WHERE release_id=%s;"

        return release.db.read_data(query, (release_id,))

    @staticmethod
    def get_release_genre(release_id):
        query = "SELECT * FROM release_genre WHERE release_id=%s;"

        return release.db.read_data(query, (release_id,))

    @staticmethod
    def get_release_style(release_id):
        query = "SELECT * FROM release_style WHERE release_id=%s;"

        return release.db.read_data(query, (release_id,))

    @staticmethod
    def get_release_label(release_id):
        query = "SELECT * FROM release_label WHERE release_id=%s;"

        return release.db.read_data(query, (release_id,))

    @staticmethod
    def get_release_artist(release_id):
        query = "SELECT * FROM release_artist WHERE release_id=%s;"

        return release.db.read_data(query, (release_id,))

    @staticmethod
    def get_release_track_artist(release_id):
        query = "SELECT * FROM release_track_artist WHERE release_id=%s;"

        return release.db.read_data(query, (release_id,))

    @staticmethod
    def get_release_format(release_id):
        query = "SELECT * FROM release_format WHERE release_id=%s;"

        return release.db.read_data(query, (release_id,))

    @staticmethod
    def get_release_identifier(release_id):
        query = "SELECT * FROM release_identifier WHERE release_id=%s;"

        return release.db.read_data(query, (release_id,))

    @staticmethod
    def get_release_video(release_id):
        query = "SELECT * FROM release_video WHERE release_id=%s;"

        return release.db.read_data(query, (release_id,))

    @staticmethod
    def get_release_company(release_id):
        query = "SELECT * FROM release_company WHERE release_id=%s;"

        return release.db.read_data(query, (release_id,))

    @staticmethod
    def get_release_image(release_id):
        query = "SELECT * FROM release_image WHERE release_id=%s;"

        return release.db.read_data(query, (release_id,))

    @classmethod
    def set_db_for_testing(cls, dbname='test_discogs_db', user='postgres', 
                         password='postgres', host='localhost', port='5433'):
        cls.db = db_utils(dbname=dbname, user=user, password=password, 
                         host=host, port=port)
        
    @classmethod
    def reset_db(cls):
        cls.db = db_utils(dbname='discogs_db', user='postgres')