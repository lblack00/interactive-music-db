# This file was written by Lucas Black
import discogs_client
import json
import os
import psycopg
import time
import redis
import requests
import sys
import secrets
from flask import Flask, jsonify, request, session, make_response
from flask_mail import Mail, Message
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity, create_access_token
from datetime import timedelta, datetime
from flask_cors import cross_origin
from functools import wraps

app = Flask(__name__)
app.secret_key = os.urandom(16)

# Session configuration
app.config['SESSION_COOKIE_SECURE'] = False  # Set to True in production with HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['SESSION_COOKIE_DOMAIN'] = 'localhost'
app.config['SESSION_COOKIE_PATH'] = '/'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)  # Session lasts 7 days

# Mail Configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'  
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'jax.395629@gmail.com'  
app.config['MAIL_PASSWORD'] = 'enddzwbchwjiyzev'     # Set by us
mail = Mail(app)
CHECK_EMAIL_VERIFICATION = True

# JWT Configuration
app.config["JWT_SECRET_KEY"] = "your-secret-key"  # Change this to a secure secret key
jwt = JWTManager(app)

# Redis for tracking logon attempts
redis_client = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)

# Login limitting
ALLOWED_LOGIN_ATTEMPTS = 3
LOCKOUT_DURATION = 60 * 1  # One minute time out

# Enable CORS so our frontend application can access backend end-points
CORS(app, 
    resources={r'/*': {'origins': 'http://localhost:5173'}},
    supports_credentials=True,
    expose_headers=['Set-Cookie'],
    allow_headers=['Content-Type', 'Authorization', 'Access-Control-Allow-Credentials', 'Access-Control-Allow-Origin'])

# Discogs API
consumer_key = "JJCOegYnRLCLRejtcZbo"
consumer_secret = "UFlGrCViqSkoBNfRTGZyUfmpTGNbFbMM"
user_agent = "PassTheAux/1.0"
token_file = "discogs_auth.json"

authenticate_discogs_API = True
discogs_client_instance = None

# source: https://github.com/jesseward/discogs-oauth-example
def save_tokens(token, secret):
    """Save access token and secret to a file"""
    with open(token_file, "w") as f:
        json.dump({"token": token, "secret": secret}, f)

def load_tokens():
    """Load stored OAuth tokens if available"""
    if os.path.exists(token_file):
        with open(token_file, "r") as f:
            return json.load(f)
    return None

def authenticate_discogs():
    """Handles OAuth authentication and reuses stored tokens."""
    global discogs_client_instance  # Use the global variable

    client = discogs_client.Client(user_agent)
    client.set_consumer_key(consumer_key, consumer_secret)
    
    tokens = load_tokens()
    if tokens:
        print("Using stored OAuth tokens.")
        try:
            client.set_token(tokens["token"], tokens["secret"])
            user = client.identity()  # Verify the token works
            print(f"Authenticated as: {user.username}")
            discogs_client_instance = client
            return client
        except HTTPError:
            print("Stored tokens are invalid. Re-authenticating...")

    # Perform full OAuth authentication
    token, secret, url = client.get_authorize_url()

    print(f"Please visit the following URL to authorize: {url}")
    oauth_verifier = input("Enter the verification code: ").strip()

    try:
        access_token, access_secret = client.get_access_token(oauth_verifier)
        save_tokens(access_token, access_secret)
        print("Authentication successful and tokens saved!")
        discogs_client_instance = client
        return client
    except HTTPError:
        print("Unable to authenticate.")
        sys.exit(1)

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

    @staticmethod
    def get_discogs_api_release(release_id):
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

class master:
    db = db_utils(dbname='discogs_db', user='postgres')

    @staticmethod
    def get_discogs_api_master(master_id):
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

class artist:
    db = db_utils(dbname='discogs_db', user='postgres')

    @staticmethod
    def get_discogs_api_artist(artist_id):
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
                   VALUES (%s, %s, %s)
                   RETURNING id;"""

        result = users.db.mutate_data(query, (username, email, hashpass))
        return result[0][0] if result else None

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

    @staticmethod
    def is_user_admin(username):
        query = "SELECT is_admin FROM users WHERE username=%s;"

        return users.db.read_data(query, (username,))[0]['is_admin']

class forum:
    db = db_utils(dbname='users_db', user='postgres')

    @staticmethod
    def get_all_threads(category=None, limit=20, offset=0):
        if category:
            query = """
                SELECT 
                    t.id, 
                    t.title, 
                    t.category,
                    t.created_at, 
                    t.updated_at,
                    t.is_edited,
                    u.id as author_id, 
                    u.username as author_name,
                        (SELECT COUNT(*)
                         FROM forum_replies r
                         WHERE r.thread_id = t.id AND r.is_deleted = FALSE) as reply_count
                FROM forum_threads t
                JOIN users u ON t.user_id = u.id
                WHERE t.is_deleted = FALSE AND t.category = %s
                ORDER BY t.created_at DESC
                LIMIT %s OFFSET %s;
            """
            return forum.db.read_data(query, (category, limit, offset))
        else:
            query = """
                SELECT 
                    t.id, 
                    t.title,
                    t.category,
                    t.created_at, 
                    t.updated_at,
                    t.is_edited,
                    u.id as author_id, 
                    u.username as author_name,
                        (SELECT COUNT(*)
                         FROM forum_replies r
                         WHERE r.thread_id = t.id AND r.is_deleted = FALSE) as reply_count
                FROM forum_threads t
                JOIN users u ON t.user_id = u.id
                WHERE t.is_deleted = FALSE
                ORDER BY t.created_at DESC
                LIMIT %s OFFSET %s;
            """
            return forum.db.read_data(query, (limit, offset))
    
    @staticmethod
    def get_categories():
        query = """
            SELECT DISTINCT category FROM forum_threads
            WHERE is_deleted = FALSE
            ORDER BY category;
        """
        return forum.db.read_data(query)
    
    @staticmethod
    def create_thread(user_id, title, content, category):
        query = """
            INSERT INTO forum_threads (user_id, title, content, category, created_at)
            VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP)
            RETURNING id;
        """
        return forum.db.mutate_data(query, (user_id, title, content, category))
    
    @staticmethod
    def get_thread(thread_id):
        query = """
            SELECT 
                t.id,
                t.title,
                t.content,
                t.category,
                t.created_at,
                t.updated_at,
                t.is_deleted,
                u.id as author_id, 
                u.username as author_name
            FROM forum_threads t
            JOIN users u ON t.user_id = u.id
            WHERE t.id = %s AND t.is_deleted = FALSE;
        """
        return forum.db.read_data(query, (thread_id,))
    
    @staticmethod
    def get_thread_replies(thread_id):
        query = """
            SELECT 
                r.id, 
                r.content, 
                r.created_at, 
                r.updated_at,
                r.parent_id,
                r.is_edited,
                u.id as author_id, 
                u.username as author_name
            FROM forum_replies r
            JOIN users u ON r.user_id = u.id
            WHERE r.thread_id = %s AND r.is_deleted = FALSE
            ORDER BY r.created_at ASC;
        """
        return forum.db.read_data(query, (thread_id,))

    @staticmethod
    def get_thread_reply(reply_id):
        query = """
            SELECT
                r.id,
                r.thread_id,
                r.content,
                r.parent_id,
                r.created_at,
                r.is_edited,
                r.is_deleted,
                u.username as author_name,
                t.title
            FROM forum_replies r
            JOIN users u
            ON r.user_id = u.id
            JOIN forum_threads t
            ON r.thread_id = t.id
            WHERE r.id = %s;
        """
        return forum.db.read_data(query, (reply_id,))
    
    @staticmethod
    def add_reply(user_id, thread_id, content, parent_id=None):
        query = """
            INSERT INTO forum_replies (user_id, thread_id, content, parent_id, created_at)
            VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP)
            RETURNING id;
        """
        return forum.db.mutate_data(query, (user_id, thread_id, content, parent_id))
    
    @staticmethod
    def update_reply(reply_id, content, user_id):
        query = """
            UPDATE forum_replies
            SET content = %s, updated_at = CURRENT_TIMESTAMP, is_edited = TRUE
            WHERE id = %s AND user_id = %s
            RETURNING id;
        """
        return forum.db.mutate_data(query, (content, reply_id, user_id))
    
    @staticmethod
    def delete_reply(reply_id, user_id):
        query = """
            UPDATE forum_replies
            SET is_deleted = TRUE, updated_at = CURRENT_TIMESTAMP
            WHERE id = %s AND user_id = %s
            RETURNING id;
        """
        return forum.db.mutate_data(query, (reply_id, user_id))
    
    @staticmethod
    def update_thread(thread_id, content, user_id):
        query = """
            UPDATE forum_threads
            SET content = %s, updated_at = CURRENT_TIMESTAMP, is_edited = TRUE
            WHERE id = %s AND user_id = %s
            RETURNING id;
        """
        return forum.db.mutate_data(query, (content, thread_id, user_id))
    
    @staticmethod
    def delete_thread(thread_id, user_id):
        query = """
            UPDATE forum_threads
            SET is_deleted = TRUE, updated_at = CURRENT_TIMESTAMP
            WHERE id = %s AND user_id = %s
            RETURNING id;
        """
        return forum.db.mutate_data(query, (thread_id, user_id))
    
    @staticmethod
    def report_item(user_id, item_type, item_id, reason):
        query = """
            INSERT INTO forum_reports (user_id, item_type, item_id, reason, created_at)
            VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP)
            RETURNING id;
        """
        return forum.db.mutate_data(query, (user_id, item_type, item_id, reason))

    @staticmethod
    def get_reports():
        query = """
            SELECT *
            FROM forum_reports
            ORDER BY created_at DESC;
        """
        reports = forum.db.read_data(query)
        content = []
        for report in reports:
            if report['item_type'] == 'thread':
                content.append(forum.get_thread(report['item_id'])[0])
            else:
                content.append(forum.get_thread_reply(report['item_id'])[0])

        return {
            'reports': reports,
            'content': content
        }

    @staticmethod
    def add_reference(item_type, item_id, reference_type, reference_id, name):
        query = """
            INSERT INTO forum_references(item_type, item_id, reference_type, reference_id, created_at, name)
            VALUES(%s, %s, %s, %s, CURRENT_TIMESTAMP, %s)
            RETURNING id;
        """
        return forum.db.mutate_data(query, (item_type, item_id, reference_type, reference_id, name))

    @staticmethod
    def delete_reference(_id, reference_id):
        query = """
            DELETE FROM forum_references fr
            WHERE id=%s AND reference_id=%s
            RETURNING id;
        """
        return forum.db.mutate_data(query, (_id, reference_id))

    @staticmethod
    def get_thread_references(item_id):
        query = """
            SELECT
                *
            FROM forum_references fr
            WHERE fr.item_id = %s;
        """
        return forum.db.read_data(query, (item_id))

    @staticmethod
    def get_reference(reference_id):
        query = """
            SELECT
                *
            FROM forum_references fr
            WHERE fr.reference_id = %s;
        """
        return forum.db.read_data(query, (reference_id))

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
                'company': release.get_release_company(release_id),
                'api_data': release.get_discogs_api_release(release_id),
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
                'release': release.get_release(main_release_id),
                'api_data': master.get_discogs_api_master(master_id),
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
                'discography': artist.get_discography(artist_id),
                'api_data': artist.get_discogs_api_artist(artist_id)
            }
        }

        return jsonify(data)

@app.route('/artist-discography-images', methods=['GET'])
def get_artist_discography_images():
    if request.method == 'GET':
        artist_id = int(request.args.get('artist_id'))

        discography = artist.get_discography(artist_id)
        discography_image_uris = {}
        for m in discography:
            image_uris = None
            discogs_response = master.get_discogs_api_master(m["id"])

            if discogs_response and 'images' in discogs_response:
                image_uris = discogs_response['images']

            if image_uris and len(image_uris) > 0:
                discography_image_uris[m["id"]] = image_uris[0]["uri"]

        data = {
            'payload': discography_image_uris
        }

        return jsonify(data)

@app.route('/get-master-image', methods=['GET'])
def get_master_image():
    if request.method == 'GET':
        master_id = int(request.args.get('master_id'))
        image_uri = master.get_discogs_api_master(master_id)

        if image_uri and len(image_uri) > 0 and 'images' in image_uri:
            data = {
                'payload': image_uri['images'][0]['uri']
            }

            return jsonify(data)
        return jsonify({})

@app.route('/get-artist-image', methods=['GET'])
def get_artist_image():
    if request.method == 'GET':
        artist_id = int(request.args.get('artist_id'))
        image_uri = artist.get_discogs_api_artist(artist_id)

        if image_uri and len(image_uri) > 0 and 'images' in image_uri:
            data = {
                'payload': image_uri['images'][0]['uri']
            }

            return jsonify(data)
        return jsonify({})

# Login limitting methods
def get_client_identifier():
    return request.remote_addr

def get_login_attempt_key(identifier, username=None):
    if username:
        return f"login_attempts:{identifier}:{username}"
    return f"login_attempts:{identifier}"

def record_failed_login(identifier, username=None):
    ip_key = get_login_attempt_key(identifier)
    redis_client.incr(ip_key)
    redis_client.expire(ip_key, LOCKOUT_DURATION)

    if username:
        user_key = get_login_attempt_key(identifier, username)
        redis_client.incr(user_key)
        redis_client.expire(user_key, LOCKOUT_DURATION)

def is_login_blocked(identifier, username=None):
    # Prevents rapid attempts from same IP
    ip_key = get_login_attempt_key(identifier)
    ip_attempts = int(redis_client.get(ip_key) or 0)
    
    if ip_attempts >= ALLOWED_LOGIN_ATTEMPTS * 2:
        return True, get_remaining_lockout_time(ip_key)
    
    # Check redis key w/ username for throttling
    if username:
        user_key = get_login_attempt_key(identifier, username)
        user_attempts = int(redis_client.get(user_key) or 0)
        
        if user_attempts >= ALLOWED_LOGIN_ATTEMPTS:
            return True, get_remaining_lockout_time(user_key)
    
    return False, 0

def reset_login_attempts(identifier, username=None):
    if username:
        user_key = get_login_attempt_key(identifier, username)
        redis_client.delete(user_key)

def get_remaining_lockout_time(key):
    return redis_client.ttl(key)

def log_security_event(event_type, username, ip_address, details=None):
    event = {
        'timestamp': datetime.now().isoformat(),
        'event_type': event_type,
        'username': username,
        'ip_address': ip_address,
        'details': details or {}
    }
    # Justs prints to console but for real production systems:
    # ** Store logs into database
    # ** Send alerts to some monitoring system and alert adminstrators
    print(f"SECURITY EVENT: {json.dumps(event)}")

@app.route('/signup', methods=['GET', 'POST', 'OPTIONS'])
def user_signup():
    if request.method == 'POST':
        print("1. Starting signup process...")
        resp = json.loads(request.data)

        username = resp['username']
        email = resp['email']
        password = resp['password']
        print(f"2. Received data - username: {username}, email: {email}")

        if not username or not email or not password:
            return jsonify({'error': 'Missing fields'}), 400

        if users.check_username_exists(username):
            return jsonify({'error': 'Username already exists'}), 409
            
        print("3. Username check passed")
        
        # Check for existing email
        query = "SELECT * FROM users WHERE email = %s;"
        if len(db_utils(dbname='users_db', user='postgres').read_data(query, (email,))) > 0:
            return jsonify({'error': 'Email address already registered'}), 409

        print("4. Email check passed")

        try:
            print("5. Starting user creation...")
            verification_token = secrets.token_urlsafe(32)
            token_expiry = datetime.now() + timedelta(hours=24)

            hashed_pass = generate_password_hash(password)
            print("6. Password hashed")

            user_id = users.create_new_user(username, email, hashed_pass)
            print(f"7. User created with ID: {user_id}")

            if not user_id:
                return jsonify({'error': 'Failed to create user'}), 500

            if CHECK_EMAIL_VERIFICATION:
                print("8. Storing verification token...")
                store_verification_token_query = """
                    INSERT INTO email_verification (user_id, verification_token, token_expiry)
                    VALUES (%s, %s, %s);
                """
                db_utils(dbname='users_db', user='postgres').mutate_data(
                    store_verification_token_query, 
                    (user_id, verification_token, token_expiry)
                )
                print("9. Verification token stored")

                print("10. Sending verification email...")
                verification_url = f"http://localhost:5173/verify-email?token={verification_token}"
                msg = Message(
                    'Verify your email address',
                    sender=app.config['MAIL_USERNAME'],
                    recipients=[email]
                )
                msg.body = f"""
                Welcome to Interactive Music DB!
                Please click the following link to verify your email address:
                {verification_url}
                
                This link will expire in 24 hours.
                """
                mail.send(msg)
                print("11. Verification email sent")

            return jsonify({
                'message': 'User created successfully. Please check your email to verify your account.',
                'requiresVerification': True
            }), 201

        except Exception as e:
            print(f"ERROR at step: {str(e)}")
            import traceback
            traceback.print_exc()
            return jsonify({'error': f'User signup failed: {str(e)}'}), 500

    return jsonify({}), 200

@app.route('/login', methods=['POST'])
def user_login():
    print("1. Login attempt started")
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    print(f"2. Received login attempt for username: {username}")

    client_ip = get_client_identifier()
    print(f"3. Client IP: {client_ip}")

    is_blocked, remaining_time = is_login_blocked(client_ip, username)
    print(f"4. Login blocked status: {is_blocked}")
    
    if is_blocked:
        print("5. Login blocked due to too many attempts")
        log_security_event('login_blocked', username, client_ip, {
            'reason': 'too_many_attempts',
            'remaining_lockout_time': remaining_time
        })

        return jsonify({
            'error': 'Too many failed login attempts',
            'lockout_remaining': remaining_time
        }), 429
    
    try:
        print("6. Checking user credentials")
        results = users.get_user(username)
        
        if not results:
            print("7. User not found")
            record_failed_login(client_ip, username)
            log_security_event('login_failure', username, client_ip, {'reason': 'user_not_found'})
            return jsonify({'error': 'Invalid credentials'}), 401

        if CHECK_EMAIL_VERIFICATION:
            print("8. Checking email verification")
            # Check if email is verified
            query = """
                SELECT is_verified 
                FROM email_verification 
                WHERE user_id = %s;
            """
            verification_result = db_utils(dbname='users_db', user='postgres').read_data(query, (results[0]['id'],))
            print(f"9. Verification result: {verification_result}")
            
            if not verification_result or not verification_result[0]['is_verified']:
                print("10. Email not verified")
                return jsonify({'error': 'Please verify your email before logging in'}), 403

        print("11. Checking password")
        # Check password
        if check_password_hash(results[0]['password'], password):
            print("12. Password correct, creating session")
            # Clear session and reset login attempts
            session.clear()
            session.permanent = True  # Make the session permanent
            session['user'] = {
                'id': results[0]['id'],
                'username': results[0]['username'],
                'email': results[0]['email']
            }

            reset_login_attempts(client_ip, username)
            print("13. Login successful")
            log_security_event('login_success', username, client_ip)
            
            response = jsonify({'message': 'Login successful'})
            return response, 200
        else:
            print("12. Password incorrect")
            record_failed_login(client_ip, username)
            return jsonify({'error': 'Invalid credentials'}), 401

    except Exception as e:
        print(f"Login error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': 'Login failed'}), 500

@app.route('/logout', methods=['POST'])
def user_logout():
    username = session.get('user', {}).get('username')
    client_ip = get_client_identifier()

    session.clear()
    response = jsonify({'message': 'Logged out successfully'})
    response.delete_cookie('session')

    if username:
        log_security_event('logout', username, client_ip)

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

@app.route('/search/reference', methods=['GET'])
def forum_search_reference():
    query = request.args.get('query', '')
    type = request.args.get('type', 'all')

    if not query:
        return jsonify({'results': []}), 200

    results = []

    if type == 'artist' or type == 'all':
        artists = search.search_artist(query)
        for artist in artists:
            results.append({
                'id': artist['id'],
                'name': artist['name'],
                'type': 'artist'
            })
    if type == 'release' or type == 'all':
        releases = search.search_release(query)
        for release in releases:
            results.append({
                'id': release['id'],
                'name': release['title'],
                'artist': release['artists'],
                'year': release['year'],
                'type': 'release'
            })

    return jsonify({'results': results}), 200

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
            print("testing")
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

# Written by Lucas Black
@app.route('/forum/threads', methods=['GET'])
def get_all_threads():
    try:
        category = request.args.get('category')
        limit = int(request.args.get('limit', 20))
        offset = int(request.args.get('offset', 0))
        
        threads = forum.get_all_threads(category, limit, offset)
        
        formatted_threads = []
        for thread in threads:
            formatted_thread = {
                "id": thread['id'],
                "title": thread['title'],
                "category": thread['category'],
                "date": thread['created_at'].strftime("%B %d, %Y") \
                        if isinstance(thread['created_at'], datetime) else thread['created_at'],
                "isEdited": thread.get('is_edited', False),
                "author": {
                    "id": thread['author_id'],
                    "name": thread['author_name']
                },
                "replies": thread['reply_count']
            }
            formatted_threads.append(formatted_thread)
        
        return jsonify(formatted_threads), 200
        
    except Exception as e:
        print(f"Error fetching threads: {e}")
        return jsonify({"error": "Internal server error", "message": str(e)}), 500

# Written by Lucas Black
@app.route('/forum/categories', methods=['GET'])
def get_forum_categories():
    try:
        categories = forum.get_categories()
        category_list = [cat['category'] for cat in categories]
        return jsonify(category_list), 200

    except Exception as e:
        print(f"Error fetching categories: {e}")
        return jsonify({"error": "Internal server error", "message": str(e)}), 500

# Written by Lucas Black
@app.route('/forum/thread', methods=['POST'])
def create_forum_thread():
    if 'user' not in session:
        return jsonify({"error": "Not logged in"}), 401

    data = request.get_json()
    user_id = session['user']['id']
    title = data.get('title')
    content = data.get('content')
    category = data.get('category')

    if not title or not content or not category:
        return jsonify({"error": "Missing required fields"}), 400

    if len(title) > 100:
        return jsonify({"error": "Title must be less than 100 characters"}), 400

    try:
        result = forum.create_thread(user_id, title, content, category)
        
        if result:
            thread_id = result[0][0]

            thread_data = forum.get_thread(thread_id)

            if thread_data:
                formatted_thread = {
                    "id": thread_data[0]['id'],
                    "title": thread_data[0]['title'],
                    "category": thread_data[0]['category'],
                    "content": thread_data[0]['content'],
                    "date": thread_data[0]['created_at'].strftime("%B %d, %Y") if isinstance(thread_data[0]['created_at'], datetime) else thread_data[0]['created_at'],
                    "author": {
                        "id": thread_data[0]['author_id'],
                        "name": thread_data[0]['author_name']
                    },
                    "replies": 0
                }
                return jsonify(formatted_thread), 201
        else:
            return jsonify({"error": "Failed to create thread"}), 500

    except Exception as e:
        print(f"Error creating thread: {e}")
        return jsonify({"error": "Internal server error", "message": str(e)}), 500

# Written by Lucas Black
@app.route('/forum/thread/<int:thread_id>', methods=['GET'])
def get_forum_thread(thread_id):
    try:
        thread_data = forum.get_thread(thread_id)
        if not thread_data:
            return jsonify({"error": "Thread not found"}), 404
            
        replies = forum.get_thread_replies(thread_id)
        references = []
        references = forum.get_thread_references(thread_id)
        
        # Format the thread data
        formatted_thread = {
            "id": thread_data[0]['id'],
            "title": thread_data[0]['title'],
            "content": thread_data[0]['content'],
            "date": thread_data[0]['created_at'].strftime("%B %d, %Y") if isinstance(thread_data[0]['created_at'], datetime) else thread_data[0]['created_at'],
            "isEdited": thread_data[0].get('is_edited', False),
            "author": {
                "id": thread_data[0]['author_id'],
                "name": thread_data[0]['author_name']
            },
            "replies": [],
            "references": references
        }
        
        # Format the replies
        for reply in replies:
            formatted_reply = {
                "id": reply['id'],
                "content": reply['content'],
                "date": reply['created_at'].strftime("%B %d, %Y") if isinstance(reply['created_at'], datetime) else reply['created_at'],
                "isEdited": reply.get('is_edited', False),
                "parentId": reply['parent_id'],
                "author": {
                    "id": reply['author_id'],
                    "name": reply['author_name']
                }
            }
            formatted_thread["replies"].append(formatted_reply)
        
        return jsonify(formatted_thread), 200
        
    except Exception as e:
        print(f"Error fetching thread: {e}")
        return jsonify({"error": "Internal server error", "message": str(e)}), 500

# Written by Lucas Black
@app.route('/forum/thread/<int:thread_id>/reply', methods=['POST'])
def add_thread_reply(thread_id):
    if 'user' not in session:
        return jsonify({"error": "Not logged in"}), 401
        
    data = request.get_json()
    user_id = session['user']['id']
    content = data.get('content')
    parent_id = data.get('parentId')
    
    if not content:
        return jsonify({"error": "Reply content cannot be empty"}), 400
        
    try:
        result = forum.add_reply(user_id, thread_id, content, parent_id)
        
        if result:
            reply_id = result[0][0]  # Extract ID from result

            replies = forum.get_thread_replies(thread_id)
            new_reply = next((r for r in replies if r['id'] == reply_id), None)
            
            if new_reply:
                formatted_reply = {
                    "id": new_reply['id'],
                    "content": new_reply['content'],
                    "date": new_reply['created_at'].strftime("%B %d, %Y") if isinstance(new_reply['created_at'], datetime) else new_reply['created_at'],
                    "isEdited": new_reply.get('is_edited', False),
                    "parentId": new_reply['parent_id'],
                    "author": {
                        "id": new_reply['author_id'],
                        "name": new_reply['author_name']
                    }
                }
                return jsonify(formatted_reply), 201
                
        return jsonify({"error": "Failed to add reply"}), 500
        
    except Exception as e:
        print(f"Error adding reply: {e}")
        return jsonify({"error": "Internal server error", "message": str(e)}), 500

# Written by Lucas Black
@app.route('/forum/reply/<int:reply_id>', methods=['PUT', 'DELETE'])
def update_delete_reply(reply_id):
    if 'user' not in session:
        return jsonify({"error": "Not logged in"}), 401
        
    user_id = session['user']['id']
    
    try:
        if request.method == 'PUT':
            data = request.get_json()
            content = data.get('content')
            
            if not content:
                return jsonify({"error": "Reply content cannot be empty"}), 400
                
            result = forum.update_reply(reply_id, content, user_id)
            
            if result:
                return jsonify({"message": "Reply updated successfully"}), 200
            return jsonify({"error": "Failed to update reply or not authorized"}), 403
            
        elif request.method == 'DELETE':
            result = forum.delete_reply(reply_id, user_id)
            
            if result:
                return jsonify({"message": "Reply deleted successfully"}), 200
            return jsonify({"error": "Failed to delete reply or not authorized"}), 403
            
    except Exception as e:
        print(f"Error updating/deleting reply: {e}")
        return jsonify({"error": "Internal server error", "message": str(e)}), 500

# Written by Lucas Black
@app.route('/forum/thread/<int:thread_id>', methods=['PUT', 'DELETE'])
def update_delete_thread(thread_id):
    if 'user' not in session:
        return jsonify({"error": "Not logged in"}), 401
        
    user_id = session['user']['id']
    
    try:
        if request.method == 'PUT':
            data = request.get_json()
            content = data.get('content')
            
            if not content:
                return jsonify({"error": "Thread content cannot be empty"}), 400
                
            result = forum.update_thread(thread_id, content, user_id)
            
            if result:
                return jsonify({"message": "Thread updated successfully"}), 200
            return jsonify({"error": "Failed to update thread or not authorized"}), 403
            
        elif request.method == 'DELETE':
            result = forum.delete_thread(thread_id, user_id)
            
            if result:
                return jsonify({"message": "Thread deleted successfully"}), 200
            return jsonify({"error": "Failed to delete thread or not authorized"}), 403
            
    except Exception as e:
        print(f"Error updating/deleting thread: {e}")
        return jsonify({"error": "Internal server error", "message": str(e)}), 500

# Written by Lucas Black
@app.route('/forum/report', methods=['POST'])
def report_forum_item():
    if 'user' not in session:
        return jsonify({"error": "Not logged in"}), 401
        
    data = request.get_json()
    user_id = session['user']['id']
    item_type = data.get('type')
    item_id = data.get('itemId')
    reason = data.get('reason')
    
    if not item_type or not item_id or not reason:
        return jsonify({"error": "Missing required fields"}), 400
        
    try:
        result = forum.report_item(user_id, item_type, item_id, reason)
        
        if result:
            return jsonify({"message": "Report submitted successfully"}), 201
        return jsonify({"error": "Failed to submit report"}), 500
        
    except Exception as e:
        print(f"Error submitting report: {e}")
        return jsonify({"error": "Internal server error", "message": str(e)}), 500

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user' not in session:
            return jsonify({"error": "Admin access required"}), 403

        user = session['user']
        if not user or not users.is_user_admin(session['user']['username']):
            return jsonify({"error": "Admin access required"}), 403
        return f(*args, **kwargs)
    return decorated

@app.route('/admin/reports', methods=['GET'])
@admin_required
def get_forum_reports():
    try:
        forum_reports = forum.get_reports()
        if forum_reports is not None:
            return jsonify(forum_reports), 200
        return jsonify({"error": "Database error fetching reports"}), 500
    except Exception as e:
        print(f"Error fetching reports: {e}")
        return jsonify({"error": "Internal server error", "message": str(e)}), 500

@app.route('/forum/reference', methods=['POST'])
def add_forum_reference():
    if 'user' not in session:
        return jsonify({'error': 'Not logged in'})

    if request.method == 'POST':
        data = request.get_json()
        item_type = data.get('item_type')
        item_id = data.get('item_id')
        reference_type = data.get('reference_type')
        reference_id = data.get('reference_id')
        reference_name = data.get('reference_name')

        if not all([item_type, item_id, reference_type, reference_id]):
            return jsonify({'error'})

        if item_type == 'thread':
            thread = forum.get_thread(item_id)
            if not thread or thread[0]['author_id'] != session['user']['id']:
                return jsonify({'error': 'Not authorized'}), 402

        try:
            result = forum.add_reference(item_type,
                                        item_id,
                                        reference_type,
                                        reference_id,
                                        reference_name)
            if result:
                return jsonify({'success': True, 'reference': result}), 201
            else:
                return jsonify({'error': 'Failed to add reference'}), 500
        except Exception as e:
            print(f'Error adding reference: {e}')
            return jsonify({'error': 'Internal server error'}), 500

@app.route('/forum/delete-reference/<int:reference_id>', methods=['DELETE'])
def delete_forum_reference(reference_id):
    if 'user' not in session:
        return jsonify({'error': 'Not logged in'})

    if request.method == 'DELETE':
        reference = forum.get_reference(reference_id)
        try:
            if not reference:
                return jsonify({'error': 'Reference not found'}), 404

            if reference[0]['item_type'] == 'thread':
                thread = forum.get_thread(reference[0]['item_id'])
                if not thread or thread[0]['author_id'] != session['user']['id']:
                    return jsonify({'error': 'Not authorized'}), 403

            result = forum.delete_reference(reference[0]['id'], reference_id)
            if result:
                return jsonify({'success': True}), 200
            else:
                return jsonify({'error': 'Failed to delete reference'}), 500
        except Exception as e:
            print(f'Error deleting reference: {e}')
            return jsonify({'error': 'Internal server error'}), 500
    
@app.route('/verify-email', methods=['GET'])
def verify_email():
    token = request.args.get('token')
    if not token:
        return jsonify({'error': 'Missing verification token'}), 400

    try:
        # Check if token exists and is valid
        query = """
            UPDATE email_verification 
            SET is_verified = TRUE 
            WHERE verification_token = %s 
            AND token_expiry > CURRENT_TIMESTAMP 
            AND is_verified = FALSE 
            RETURNING user_id;
        """
        result = db_utils(dbname='users_db', user='postgres').mutate_data(query, (token,))

        if result:
            return jsonify({'message': 'Email verified successfully'}), 200
        else:
            return jsonify({'error': 'Invalid or expired verification token'}), 400

    except Exception as e:
        print(f"Verification error: {e}")
        return jsonify({'error': 'Verification failed'}), 500
    
@app.route('/request-password-reset', methods=['POST'])
def request_password_reset():
    data = request.get_json()
    email = data.get('email')
    
    if not email:
        return jsonify({'error': 'Email is required'}), 400
        
    try:
        # Check if user exists
        query = "SELECT id, username FROM users WHERE email = %s;"
        result = db_utils(dbname='users_db', user='postgres').read_data(query, (email,))
        
        if result:
            # Generate reset token
            reset_token = secrets.token_urlsafe(32)
            expiry = datetime.now() + timedelta(hours=1)
            
            # Store reset token
            store_token_query = """
                INSERT INTO password_reset_tokens (user_id, token, expiry)
                VALUES (%s, %s, %s)
                ON CONFLICT (user_id) DO UPDATE
                SET token = EXCLUDED.token, expiry = EXCLUDED.expiry;
            """
            db_utils(dbname='users_db', user='postgres').mutate_data(
                store_token_query, 
                (result[0]['id'], reset_token, expiry)
            )
            
            # Send reset email
            reset_url = f"http://localhost:5173/reset-password?token={reset_token}"
            msg = Message(
                'Password Reset Request',
                sender=app.config['MAIL_USERNAME'],
                recipients=[email]
            )
            msg.body = f"""
            Hello {result[0]['username']},
            
            You have requested to reset your password. Please click the following link to reset your password:
            {reset_url}
            
            This link will expire in 1 hour.
            
            If you did not request this reset, please ignore this email.
            """
            mail.send(msg)
        
        # Always return success to prevent email enumeration
        return jsonify({'message': 'If an account exists with this email, you will receive reset instructions.'}), 200
        
    except Exception as e:
        print(f"Password reset error: {str(e)}")
        return jsonify({'error': 'Failed to process reset request'}), 500
    
if __name__ == "__main__":
    if authenticate_discogs_API:
        authenticate_discogs()
    app.run(port=5001, debug=True)
