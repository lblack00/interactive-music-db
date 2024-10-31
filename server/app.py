import psycopg
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(__name__)

# Enable CORS so our frontend application can access backend end-points
CORS(app, resources={r'/*': {'origins': '*'}})

# Class for handling DB connections and operations with psycopg
class db_utils:
    def __init__(self, dbname, user):
        self.dbname = dbname
        self.user = user

    def read_data(self, query=""):
        conn = psycopg.Connection.connect("dbname=%s user=%s" % (self.dbname, self.user),
            row_factory=psycopg.rows.dict_row)

        results = []
        with conn.cursor() as cur:
            # could add a database logger here
            cur.execute(query)
            results = cur.fetchall()

        conn.close()

        return results

    def mutate_data(self, query=""):
        conn = psycopg.Connection.connect("dbname=%s user=%s" % (self.dbname, self.user),
            row_factory=psycopg.rows.dict_row)

        results = []
        with conn.cursor() as cur:
            # could add a database logger here
            cur.execute(query)
            results = cur.fetchall()

        conn.commit()
        conn.close()

        return results

# Class for building SQL queries and handing them to database connection
class discogs:
    db = db_utils(dbname='discogs_db', user='postgres')

    # def get_track_credits(track_id):
    @staticmethod
    def get_all_versions_of_master(master_id):
        query = "SELECT * FROM release WHERE master_id=%d;" % master_id

        return discogs.db.read_data(query)

    @staticmethod
    def get_all_master_releases_from_artist(artist_name):
        query = """SELECT * FROM master_artist
                   JOIN master ON master.id=master_artist.master_id
                   WHERE artist_name='%s';""" % artist_name

        return discogs.db.read_data(query)

    @staticmethod
    def get_release(release_id):
        # todo: need to sanitize SQL input from a user
        query = "SELECT * FROM release WHERE id=%d;" % release_id

        return discogs.db.read_data(query)

    @staticmethod
    def get_release_tracklist(release_id):
        # todo: need to sanitize SQL input from a user
        query = "SELECT * FROM release_track WHERE release_id=%d;" % release_id

        return discogs.db.read_data(query)

    @staticmethod
    def get_release_genre(release_id):
        query = "SELECT * FROM release_genre WHERE release_id=%d;" % release_id

        return discogs.db.read_data(query)

    @staticmethod
    def get_release_style(release_id):
        query = "SELECT * FROM release_style WHERE release_id=%d;" % release_id

        return discogs.db.read_data(query)

    @staticmethod
    def get_release_label(release_id):
        query = "SELECT * FROM release_label WHERE release_id=%d;" % release_id

        return discogs.db.read_data(query)

    @staticmethod
    def get_release_artist(release_id):
        query = "SELECT * FROM release_artist WHERE release_id=%d;" % release_id

        return discogs.db.read_data(query)

    @staticmethod
    def get_release_track_artist(release_id):
        query = "SELECT * FROM release_track_artist WHERE release_id=%d;" % release_id

        return discogs.db.read_data(query)

    @staticmethod
    def get_release_format(release_id):
        query = "SELECT * FROM release_format WHERE release_id=%d;" % release_id

        return discogs.db.read_data(query)

    @staticmethod
    def get_release_identifier(release_id):
        query = "SELECT * FROM release_identifier WHERE release_id=%d;" % release_id

        return discogs.db.read_data(query)

    @staticmethod
    def get_release_video(release_id):
        query = "SELECT * FROM release_video WHERE release_id=%d;" % release_id

        return discogs.db.read_data(query)

    @staticmethod
    def get_release_company(release_id):
        query = "SELECT * FROM release_company WHERE release_id=%d;" % release_id

        return discogs.db.read_data(query)

    @staticmethod
    def get_release_image(release_id):
        query = "SELECT * FROM release_image WHERE release_id=%d;" % release_id

        return discogs.db.read_data(query)

@app.route('/release/', methods=['GET'])
def get_release():
    if request.method == 'GET':
        # convert parameter to integer
        release_id = int(request.args.get('release_id'))

        data = {
            'payload': {
                'release': discogs.get_release(release_id),
                'tracks': discogs.get_release_tracklist(release_id),
                'genre': discogs.get_release_genre(release_id),
                'style': discogs.get_release_style(release_id),
                'label': discogs.get_release_label(release_id),
                'artist': discogs.get_release_artist(release_id),
                'track_artist': discogs.get_release_track_artist(release_id),
                'format': discogs.get_release_format(release_id),
                'identifer': discogs.get_release_identifier(release_id),
                'video': discogs.get_release_video(release_id),
                'company': discogs.get_release_company(release_id)
            }
        }

        return jsonify(data)

@app.route('/ping', methods=['GET'])
def ping_pong():

    # conn = psycopg.Connection.connect("dbname=discogs_db user=postgres", row_factory=psycopg.rows.dict_row)
    
    # with conn.cursor() as cur:
        # query = "SELECT * FROM release"
        # query += " JOIN release_artist ON release.id=release_artist.release_id"
        # query += " JOIN release_genre ON release_genre.release_id=release.id"
        # query += " JOIN release_style ON release_style.release_id=release.id"
        # query += " WHERE release.master_id=588280"

        # query = "SELECT * FROM release_artist where artist_name='Metallica' AND tracks IS NOT NULL"

        # how to get the tracklist from an album release
        # given a tracklist where the entry for position is null, it just means it's the title of
        # following tracks
        # ex: https://www.discogs.com/release/24333857-Nirvana-In-Concert
        # query = "SELECT * FROM release_track WHERE release_id=24333857"

        # example of a single (description)
        # query = "SELECT * FROM release JOIN release_format ON release.id=release_format.release_id WHERE release.id=(SELECT main_release FROM master WHERE id=22439)"

        # example of an album
        # query = "SELECT * FROM release JOIN release_format ON release.id=release_format.release_id WHERE release.id=(SELECT main_release FROM master WHERE id=13814)"

        # tracklist of said album
        # query = "SELECT * FROM release_track WHERE release_id=(SELECT main_release FROM master WHERE id=13814)"

        # get all releases from nirvana
        # query = "SELECT * FROM master_artist JOIN master ON master.id=master_artist.master_id WHERE artist_name='Nirvana'"

        # get artists credit on a release
        # query = "SELECT * FROM release_artist WHERE release_id=367084"

        # get all versions of a type of release
        # query = "SELECT * FROM release WHERE master_id=13814"

        # sometimes credits don't come through
        # query = "SELECT * FROM release_artist WHERE release_id=6652939"

        # basically an artist's discography
        # query = "SELECT * FROM master_artist JOIN master ON master_artist.master_id=master.id "
        # query += "JOIN release ON master.main_release=release.id "
        # query += "JOIN release_genre ON release_genre.release_id=release.id "
        # query += "JOIN release_style ON release_style.release_id=release.id "
        # query += "JOIN release_format ON release.id=release_format.release_id "
        # query += "WHERE master_artist.artist_name='Metallica' AND NOT (release_format.descriptions LIKE '%Unofficial Release%')"
        
        # query = "SELECT * FROM release_track_artist WHERE artist_name='Metallica'"

    #     cur.execute(query)
    #     results = cur.fetchall()

    # conn.close()

    # results = [res for res in results if 'unoffical release' in res['descriptions'].lower()]
    # for res in results:
    #     print(res['title'])

    return jsonify(discogs.get_all_master_releases_from_artist('Nirvana'))

if __name__ == "__main__":
    app.run(debug=True)
