# This file was written by Lucas Black
from db_utils import db_utils

class search:
    db = db_utils(dbname='discogs_db', user='postgres')

    @staticmethod
    def search_artist(artist_name):
        query = "SELECT * FROM artist WHERE LOWER(name) LIKE %s ORDER BY name LIMIT 25;"
        return search.db.read_data(query, ("%" + artist_name.lower() + "%",))

    @staticmethod
    def search_release(release_name):
        query = """
            SELECT 
                m.id, 
                m.title, 
                COALESCE(m.year::text, 'N/A') as year,
                COALESCE(
                    (
                        SELECT STRING_AGG(a.name, ', ')
                        FROM master_artist ma
                        JOIN artist a ON ma.artist_id = a.id
                        WHERE ma.master_id = m.id
                    ),
                    'Unknown Artist'
                ) as artists
            FROM master m
            WHERE LOWER(m.title) LIKE %s
            ORDER BY m.year DESC
            LIMIT 25;
        """
        return search.db.read_data(query, ("%" + release_name.lower() + "%",))

    @staticmethod
    def search_track(track_name):
        query = """
            SELECT 
                rt.title as title,           -- track title
                rt.release_id,
                r.title as release_title,    -- album title
                COALESCE(r.released, 'N/A') as released  -- year with fallback
            FROM release_track rt
            JOIN release r ON rt.release_id = r.id
            WHERE LOWER(rt.title) LIKE %s
            GROUP BY rt.title, rt.release_id, r.title, r.released
            LIMIT 25;
        """
        return search.db.read_data(query, ("%" + track_name.lower() + "%",))

    @classmethod
    def set_db_for_testing(cls):
        cls.db = db_utils(dbname='test_discogs_db', user='postgres', password='postgres', 
                         host='localhost', port='5433')
        
    @classmethod
    def reset_db(cls):
        cls.db = db_utils(dbname='discogs_db', user='postgres')