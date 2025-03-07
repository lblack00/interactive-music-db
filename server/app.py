# This file was written by Lucas Black
import json
import os
import psycopg
from flask import Flask, jsonify, request, session, make_response
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity, create_access_token
from datetime import timedelta
from flask_cors import cross_origin

app = Flask(__name__)
app.secret_key = os.urandom(16)

# Session configuration
app.config['SESSION_COOKIE_SECURE'] = False  # Set to True in production with HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['SESSION_COOKIE_DOMAIN'] = 'localhost'
app.config['SESSION_COOKIE_PATH'] = '/'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)  # Session lasts 7 days

# JWT Configuration
app.config["JWT_SECRET_KEY"] = "your-secret-key"  # Change this to a secure secret key
jwt = JWTManager(app)

# Enable CORS so our frontend application can access backend end-points
CORS(app, 
    resources={r'/*': {'origins': 'http://localhost:5173'}},
    supports_credentials=True,
    expose_headers=['Set-Cookie'],
    allow_headers=['Content-Type', 'Authorization', 'Access-Control-Allow-Credentials'])

# Class for handling DB connections and operations with psycopg
class db_utils:
    def __init__(self, dbname, user):
        self.dbname = dbname
        self.user = user

    def read_data(self, query="", query_params=()):
        if not isinstance(query_params, tuple):
            query_params = (query_params,)

        conn = psycopg.Connection.connect("dbname=%s user=%s" % (self.dbname, self.user),
            row_factory=psycopg.rows.dict_row)

        results = []
        with conn.cursor() as cur:
            # could add a database logger here
            cur.execute(query, query_params)
            results = cur.fetchall()

        conn.close()

        return results

    def mutate_data(self, query="", query_params=()):
        if not isinstance(query_params, tuple):
            query_params = (query_params,)

        conn = psycopg.Connection.connect("dbname=%s user=%s" % (self.dbname, self.user))

        try:
            with conn.cursor() as cur:
                cur.execute(query, query_params)
                if cur.description:  # Check if the query returns data
                    result = cur.fetchall()  # Get any returned data
                else:
                    result = None
            conn.commit()  # Commit the transaction
            return result
        except Exception as e:
            print(f"Database error: {e}")
            conn.rollback()  # Rollback on error
            raise e
        finally:
            conn.close()

# Class for building SQL release queries and handing them to database connection
class release:
    db = db_utils(dbname='discogs_db', user='postgres')

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

class master:
    db = db_utils(dbname='discogs_db', user='postgres')

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

class artist:
    db = db_utils(dbname='discogs_db', user='postgres')

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

class users:
    db = db_utils(dbname='users_db', user='postgres')

    @staticmethod
    def create_new_user(username, email, hashpass):
        query = """INSERT INTO users (username, email, password)
                          VALUES (%s, %s, %s);"""

        users.db.mutate_data(query, (username, email, hashpass))

    @staticmethod
    def check_username_exists(username):
        query = "SELECT * FROM users WHERE username=%s;"

        return len(users.db.read_data(query, (username,))) > 0

    @staticmethod
    def validate_user(username, password):
        query = "SELECT * FROM users WHERE username=%s;"
        res = users.db.read_data(query, (username,))[0]['password']

        return check_password_hash(res, password)

    @staticmethod
    def get_user(username):
        query = "SELECT * FROM users WHERE username=%s;"

        return users.db.read_data(query, (username,))

@app.route('/release/', methods=['GET'])
def get_release():
    try:
        release_id = request.args.get('release_id')
        if not release_id:
            return jsonify({"error": "Missing release_id parameter"}), 400

        try:
            release_id = int(release_id)
        except ValueError:
            return jsonify({"error": "Invalid release_id format"}), 400

        release_data = release.get_release(release_id)
        if not release_data:
            return jsonify({"error": "Release not found"}), 404

        data = {
            'payload': {
                'release': release_data,
                'tracks': release.get_release_tracklist(release_id),
                'genre': release.get_release_genre(release_id),
                'style': release.get_release_style(release_id),
                'label': release.get_release_label(release_id),
                'artist': release.get_release_artist(release_id),
                'track_artist': release.get_release_track_artist(release_id),
                'format': release.get_release_format(release_id),
                'identifier': release.get_release_identifier(release_id),
                'video': release.get_release_video(release_id),
                'company': release.get_release_company(release_id)
            }
        }

        return jsonify(data), 200

    except Exception as e:
        return jsonify({"error": "Internal server error", "message": str(e)}), 500

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

@app.route('/artist', methods=['GET'])
def get_artist():
    if request.method == 'GET':
        artist_id = int(request.args.get('artist_id'))

        # todo: can add more here
        data = {
            'payload': {
                'artist': artist.get_artist(artist_id),
                'discography': artist.get_discography(artist_id)
            }
        }

        return jsonify(data)

@app.route('/signup', methods=['GET', 'POST', 'OPTIONS'])
def user_signup():
    if request.method == 'POST':
        resp = json.loads(request.data)

        username = resp['username']
        email = resp['email']
        password = resp['password']

        if not username or not email or not password:
            return jsonify({'error': 'Missing fields'}), 400

        hashed_pass = generate_password_hash(password)

        try:
            users.create_new_user(username, email, hashed_pass)

            results = users.get_user(username)

            session.clear()
            session.modified = True
            session.permanent = True  # Make the session permanent
            session['user'] = {
                'id': results[0]['id'],
                'username': results[0]['username'],
                'email': results[0]['email']
            }

            return jsonify({'message': 'User created successfully'}), 201
        except Exception as e:
            print(e)
            return jsonify({'error': 'User signup failed'}), 500

    return jsonify({}), 200

@app.route('/login', methods=['POST'])
def user_login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    try:
        results = users.get_user(username)
        
        if results and check_password_hash(results[0]['password'], password):
            session.clear()
            session.permanent = True  # Make the session permanent
            session['user'] = {
                'id': results[0]['id'],
                'username': results[0]['username'],
                'email': results[0]['email']
            }
            
            response = jsonify({'message': 'Login successful'})
            return response, 200
        else:
            return jsonify({'error': 'Invalid credentials'}), 401
            
    except Exception as e:
        print(f"Login error: {e}")
        return jsonify({'error': 'Server error'}), 500

@app.route('/logout', methods=['POST'])
def user_logout():
    session.clear()
    response = jsonify({'message': 'Logged out successfully'})
    response.delete_cookie('session')
    return response, 200

@app.route('/check-session', methods=['GET'])
def user_check_session():
    print("Session contents:", session)  # Debug print
    if 'user' in session:
        return jsonify({
            'logged_in': True,
            'user': session['user']
        }), 200
    return jsonify({'logged_in': False}), 200

@app.route('/search', methods=['POST'])
def user_search():
    datum = json.loads(request.data)
    if 'filterOption' in datum:
        if datum['filterOption'].lower() == 'artists':
            results = search.search_artist(datum['query'])
            return jsonify({'results': results}), 200

        elif datum['filterOption'].lower() == 'releases':
            results = search.search_release(datum['query'])
            return jsonify({'results': results}), 200

        elif datum['filterOption'].lower() == 'tracks':
            results = search.search_track(datum['query'])
            return jsonify({'results': results}), 200

    return jsonify({'results':[]}), 200

#written by jax hendrickson
@app.route('/ratings', methods=['GET'])
def get_ratings():
    item_type = request.args.get('item_type')
    item_id = request.args.get('item_id')
    
    try:
        # Get average rating and total count
        query = """
            SELECT 
                COALESCE(ROUND(AVG(rating)::numeric, 1), 0) as average,
                COUNT(*) as total
            FROM ratings 
            WHERE item_type = %s 
            AND item_id = %s
        """
        
        result = db_utils(dbname='users_db', user='postgres').read_data(query, (item_type, item_id))
        
        if result:
            return jsonify({
                'average': float(result[0]['average']) if result[0]['average'] else 0,
                'total': result[0]['total']
            })
        return jsonify({'average': 0, 'total': 0})
        
    except Exception as e:
        print(f"Error fetching ratings: {e}")
        return jsonify({'error': 'Server error'}), 500


#written by jax hendrickson
@app.route('/user-rating', methods=['GET'])
def get_user_rating():
    if 'user' not in session:
        return jsonify({'error': 'Not logged in'}), 401
        
    item_type = request.args.get('item_type')
    item_id = request.args.get('item_id')
    user_id = session['user']['id']
    
    try:
        query = """
            SELECT rating 
            FROM ratings 
            WHERE user_id = %s 
            AND item_type = %s 
            AND item_id = %s
        """
        
        result = db_utils(dbname='users_db', user='postgres').read_data(query, (user_id, item_type, item_id))
        
        if result:
            return jsonify({'rating': result[0]['rating']}), 200
        return jsonify({'rating': 0}), 200
        
    except Exception as e:
        print(f"Error getting user rating: {e}")
        return jsonify({'error': 'Server error'}), 500

#route written by jax hendrickson
@app.route('/rate', methods=['POST'])
def rate_item():
    print("Session contents:", session)  # Debug print
    if 'user' not in session:
        return jsonify({'error': 'Not logged in'}), 401
        
    data = request.get_json()
    user_id = session['user']['id']
    item_type = data.get('item_type')
    item_id = data.get('item_id')
    rating = data.get('rating')
    
    try:
        db = db_utils(dbname='users_db', user='postgres')
        
        # First try to update existing rating
        update_query = """
            UPDATE ratings 
            SET rating = %s, updated_at = CURRENT_TIMESTAMP
            WHERE user_id = %s AND item_type = %s AND item_id = %s
            RETURNING id;
        """
        
        result = db.mutate_data(update_query, (rating, user_id, item_type, item_id))
        
        # If no existing rating, insert new one
        if not result:
            insert_query = """
                INSERT INTO ratings (user_id, item_type, item_id, rating)
                VALUES (%s, %s, %s, %s)
                RETURNING id;
            """
            
            result = db.mutate_data(insert_query, (user_id, item_type, item_id, rating))
            
        return jsonify({'success': True}), 200
        
    except Exception as e:
        print(f"Error saving rating: {e}")
        return jsonify({'error': 'Server error'}), 500

@app.route('/upcoming-releases', methods=['GET'])
@cross_origin(supports_credentials=True)
def get_upcoming_releases():
    try:
        query = """
            SELECT 
                id,
                title,
                artist,
                release_date,
                additional_info,
                source_url
            FROM upcoming_releases
            WHERE release_date >= CURRENT_DATE
            ORDER BY release_date ASC
            LIMIT 50;
        """
        
        releases = db_utils(dbname='discogs_db', user='postgres').read_data(query)
        return jsonify({"releases": releases}), 200
        
    except Exception as e:
        print(f"Error fetching releases: {e}")
        return jsonify({'error': str(e)}), 500

# Written by Matthew Stenvold
@app.route('/api/musiclist/<string:username>/<string:item_type>', methods=['GET'])
def get_user_music_list(username, item_type):
    """Fetches music ratings for a specific user and item type (master or artist)."""
    try:
        db = db_utils(dbname='users_db', user='postgres')

        # Get user_id based on username
        user_query = "SELECT id FROM users WHERE username = %s;"
        user_result = db.read_data(user_query, (username,))

        if not user_result:
            return jsonify({'error': 'User not found'}), 404

        user_id = user_result[0]['id']

        # Fetch rated items based on item_type
        query = """
            SELECT item_id, rating, created_at
            FROM ratings
            WHERE user_id = %s AND item_type = %s
            ORDER BY created_at DESC;
        """
        user_ratings = db.read_data(query, (user_id, item_type))

        if not user_ratings:
            return jsonify([]), 200  # Return empty list if no ratings exist

        # Get additional data for each rated item
        detailed_results = []

        # Different types of data have different names for "name"
        nameAlias = ""
        if item_type == "master":
            nameAlias = "title"
        elif item_type == "artist":
            nameAlias = "name"

        # TODO Change created at to updated at

        for rating in user_ratings:
            item_id = rating["item_id"]
            created_at = rating["created_at"]  # Format date without year

            if item_type == "master":
                item_info = master.get_master(item_id)
            elif item_type == "artist":
                item_info = artist.get_artist(item_id)
            else:
                continue  # Skip unknown item types

            print(item_info[0].get(nameAlias, "Unknown"))
            if item_info:
                detailed_results.append({
                    "id": item_id,
                    "name": item_info[0].get(nameAlias, "Unknown"),  # Handle missing names
                    "rating": rating["rating"],
                    "created_at": created_at,  # Date without year
                })
        print(detailed_results)
        return jsonify(detailed_results), 200

    except Exception as e:
        print(f"Error fetching music list: {e}")
        return jsonify({'error': 'Server error'}), 500
    
if __name__ == "__main__":
    app.run(port=5001, debug=True)
