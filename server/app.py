import psycopg
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)

# Enable CORS so our frontend application can access backend end-points
CORS(app, resources={r'/*': {'origins': 'http://localhost:5173'}})

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
        conn = psycopg.Connection.connect("dbname=%s user=%s" % (self.dbname, self.user))

        with conn.cursor() as cur:
            # could add a database logger here
            cur.execute(query)

        conn.commit()
        conn.close()

# Class for building SQL release queries and handing them to database connection
class release:
    db = db_utils(dbname='discogs_db', user='postgres')

    # def get_track_credits(track_id):
    @staticmethod
    def get_all_versions_of_master(master_id):
        query = "SELECT * FROM release WHERE master_id=%d;" % master_id

        return release.db.read_data(query)

    @staticmethod
    def get_release(release_id):
        # todo: need to sanitize SQL input from a user
        query = "SELECT * FROM release WHERE id=%d;" % release_id

        return release.db.read_data(query)

    @staticmethod
    def get_release_tracklist(release_id):
        # todo: need to sanitize SQL input from a user
        query = "SELECT * FROM release_track WHERE release_id=%d;" % release_id

        return release.db.read_data(query)

    @staticmethod
    def get_release_genre(release_id):
        query = "SELECT * FROM release_genre WHERE release_id=%d;" % release_id

        return release.db.read_data(query)

    @staticmethod
    def get_release_style(release_id):
        query = "SELECT * FROM release_style WHERE release_id=%d;" % release_id

        return release.db.read_data(query)

    @staticmethod
    def get_release_label(release_id):
        query = "SELECT * FROM release_label WHERE release_id=%d;" % release_id

        return release.db.read_data(query)

    @staticmethod
    def get_release_artist(release_id):
        query = "SELECT * FROM release_artist WHERE release_id=%d;" % release_id

        return release.db.read_data(query)

    @staticmethod
    def get_release_track_artist(release_id):
        query = "SELECT * FROM release_track_artist WHERE release_id=%d;" % release_id

        return release.db.read_data(query)

    @staticmethod
    def get_release_format(release_id):
        query = "SELECT * FROM release_format WHERE release_id=%d;" % release_id

        return release.db.read_data(query)

    @staticmethod
    def get_release_identifier(release_id):
        query = "SELECT * FROM release_identifier WHERE release_id=%d;" % release_id

        return release.db.read_data(query)

    @staticmethod
    def get_release_video(release_id):
        query = "SELECT * FROM release_video WHERE release_id=%d;" % release_id

        return release.db.read_data(query)

    @staticmethod
    def get_release_company(release_id):
        query = "SELECT * FROM release_company WHERE release_id=%d;" % release_id

        return release.db.read_data(query)

    @staticmethod
    def get_release_image(release_id):
        query = "SELECT * FROM release_image WHERE release_id=%d;" % release_id

        return release.db.read_data(query)

class master:
    db = db_utils(dbname='discogs_db', user='postgres')

    @staticmethod
    def get_all_master_releases_from_artist(artist_name):
        query = """SELECT * FROM master_artist
                   JOIN master ON master.id=master_artist.master_id
                   WHERE artist_name='%s';""" % artist_name

        return master.db.read_data(query)

    @staticmethod
    def get_master(master_id):
        query = "SELECT * FROM master WHERE id=%d;" % master_id

        return master.db.read_data(query)

    @staticmethod
    def get_master_artist(master_id):
        query = "SELECT * FROM master_artist WHERE master_id=%d;" % master_id

        return master.db.read_data(query)

    @staticmethod
    def get_master_video(master_id):
        query = "SELECT * FROM master_video WHERE master_id=%d;" % master_id

        return master.db.read_data(query)

    @staticmethod
    def get_master_genre(master_id):
        query = "SELECT * FROM master_genre WHERE master_id=%d;" % master_id

        return master.db.read_data(query)

    @staticmethod
    def get_master_style(master_id):
        query = "SELECT * FROM master_style WHERE master_id=%d;" % master_id

        return master.db.read_data(query)

    @staticmethod
    def get_master_release_id(master_id):
        query = "SELECT main_release FROM master WHERE id=%d;" % master_id

        return master.db.read_data(query)

@app.route('/release/', methods=['GET'])
def get_release():
    if request.method == 'GET':
        # convert parameter to integer
        release_id = int(request.args.get('release_id'))

        data = {
            'payload': {
                'release': release.get_release(release_id),
                'tracks': release.get_release_tracklist(release_id),
                'genre': release.get_release_genre(release_id),
                'style': release.get_release_style(release_id),
                'label': release.get_release_label(release_id),
                'artist': release.get_release_artist(release_id),
                'track_artist': release.get_release_track_artist(release_id),
                'format': release.get_release_format(release_id),
                'identifer': release.get_release_identifier(release_id),
                'video': release.get_release_video(release_id),
                'company': release.get_release_company(release_id)
            }
        }

        return jsonify(data)

@app.route('/master/', methods=['GET'])
def get_master():
    if request.method == 'GET':
        master_id = int(request.args.get('master_id'))
        main_release_id = master.get_master_release_id(master_id)[0]['main_release']

        data = {
            'payload': {
                'master': master.get_master(master_id),
                'artist': master.get_master_artist(master_id),
                'genre': master.get_master_genre(master_id),
                'style': master.get_master_style(master_id),
                'video': master.get_master_video(master_id),
                'tracks': release.get_release_tracklist(main_release_id),
                'label': release.get_release_label(main_release_id),
                'artist_credits': {
                    'artist': release.get_release_artist(main_release_id),
                    'track_artist': release.get_release_track_artist(main_release_id),
                },
                'format': release.get_release_format(main_release_id),
                'identifer': release.get_release_identifier(main_release_id),
                'company': release.get_release_company(main_release_id),
                'release': release.get_release(main_release_id)
            }
        }

        return jsonify(data)

@app.route('/signup', methods=['GET', 'POST', 'OPTIONS'])
def user_signup():
    if request.method == 'POST':
        print(request.data)
        return jsonify({})

    return jsonify({})

@app.route('/login', methods=['GET', 'POST', 'OPTIONS'])
def user_login():
    if request.method == 'POST':
        print(request.data)
        return jsonify({})

    return jsonify({})

if __name__ == "__main__":
    app.run(port=5001, debug=True)
