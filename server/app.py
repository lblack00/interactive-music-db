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
from flask_caching import Cache
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity, create_access_token
from datetime import timedelta, datetime
from flask_cors import cross_origin
from functools import wraps
from PIL import Image
from db_utils import db_utils
from forum import forum
from release import release
from master import master
from artist import artist
from users import users
from search import search

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
CHECK_EMAIL_VERIFICATION = False

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

authenticate_discogs_API = False
discogs_client_instance = None
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

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
                'api_data': release.get_discogs_api_release(release_id, \
                                                            authenticate_discogs_API, \
                                                            discogs_client_instance),
            }
        }

        return jsonify(data), 200

    except Exception as e:
        return jsonify({"error": "Internal server error", "message": str(e)}), 500

@app.route('/master/', methods=['GET'])
def get_master():
    try:
        master_id = request.args.get('master_id')
        if not master_id:
            return jsonify({"error": "Missing master_id parameter"}), 400

        try:
            master_id = int(master_id)
        except ValueError:
            return jsonify({"error": "Invalid master_id format"}), 400

        try:
            main_release_id = master.get_master_release_id(master_id)[0]['main_release']
        except IndexError:
            return jsonify({"error": "Master not found"}), 404

        master_data = master.get_master(master_id)
        if not master_data:
            return jsonify({"error": "Master not found"}), 404

        data = {
            'payload': {
                'master': master_data,
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
                'api_data': master.get_discogs_api_master(master_id, \
                                                          authenticate_discogs_API,
                                                          discogs_client_instance),
            }
        }

        return jsonify(data), 200
    except Exception as e:
        print(e)
        return jsonify({"error": "Internal server error", "message": str(e)}), 500

@app.route('/artist', methods=['GET'])
def get_artist():
    try:
        artist_id = request.args.get('artist_id')
        if not artist_id:
            return jsonify({"error": "Missing artist_id parameter"}), 400

        try:
            artist_id = int(artist_id)
        except ValueError:
            return jsonify({"error": "Invalid artist_id format"}), 400

        artist_data = artist.get_artist(artist_id)
        if not artist_data:
            return jsonify({"error": "Artist not found"}), 404

        # todo: can add more here
        data = {
            'payload': {
                'artist': artist.get_artist(artist_id),
                'discography': artist.get_discography(artist_id),
                'api_data': artist.get_discogs_api_artist(artist_id, \
                                                          authenticate_discogs_API, \
                                                          discogs_client_instance)
            }
        }

        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": "Internal server error", "message": str(e)}), 500

@app.route('/artist-discography-images', methods=['GET'])
@cache.cached(timeout=3600, query_string=True)
def get_artist_discography_images():
    try:
        artist_id = request.args.get('artist_id')
        if not artist_id:
            return jsonify({"error": "Missing artist_id parameter"}), 400

        try:
            artist_id = int(artist_id)
        except ValueError:
            return jsonify({"error": "Invalid artist_id format"}), 400

        discography = artist.get_discography(artist_id)
        discography_image_uris = {}
        for m in discography:
            image_uris = None
            discogs_response = master.get_discogs_api_master(m["id"], \
                                                             authenticate_discogs_API, \
                                                             discogs_client_instance)

            if discogs_response and 'images' in discogs_response:
                image_uris = discogs_response['images']

            if image_uris and len(image_uris) > 0:
                discography_image_uris[m["id"]] = image_uris[0]["uri"]

        data = {
            'payload': discography_image_uris
        }

        return jsonify(data)
    except Exception as e:
        return jsonify({"error": "Internal server error", "message": str(e)}), 500

@app.route('/get-master-image', methods=['GET'])
@cache.cached(timeout=3600, query_string=True)
def get_master_image():
    if request.method == 'GET':
        master_id = int(request.args.get('master_id'))
        image_uri = master.get_discogs_api_master(master_id, \
                                                  authenticate_discogs_API, \
                                                  discogs_client_instance)

        if image_uri and len(image_uri) > 0 and 'images' in image_uri:
            data = {
                'payload': image_uri['images'][0]['uri']
            }

            return jsonify(data)
        return jsonify({})

@app.route('/get-artist-image', methods=['GET'])
@cache.cached(timeout=3600, query_string=True)
def get_artist_image():
    try:
        if 'artist_id' not in request.args:
            return jsonify({"error": "Missing artist_id parameter"}), 400

        artist_id = request.args.get('artist_id')
        try:
            artist_id = int(artist_id)
        except ValueError:
            return jsonify({"error": "Invalid artist_id format"}), 400

        image_uri = artist.get_discogs_api_artist(artist_id)

        if image_uri and len(image_uri) > 0 and 'images' in image_uri:
            data = {
                'payload': image_uri['images'][0]['uri']
            }

            return jsonify(data), 200
        return jsonify({}), 400
    except Exception as e:
        return jsonify({"error": "Internal server error", "message": str(e)}), 500

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

@app.route('/is-session-user', methods=['GET'])
def is_session_user():
    if 'user' not in session:
        return jsonify({'match': False, 'logged_in': False}), 200

    # Extract input from query parameters
    identifier = request.args.get('identifier')
    identifier_type = request.args.get('type', 'id')  # Default to 'id'

    session_user = session['user']

    if identifier_type == 'username':
        match = str(session_user.get('username')) == str(identifier)
    else:  # Default is 'id'
        match = str(session_user.get('id')) == str(identifier)

    print(match)

    return jsonify({'match': match, 'logged_in': True}), 200

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
    
# Written by Matthew Stenvold
@app.route('/generic-user-rating', methods=['GET'])
def get_generic_user_rating():
    item_type = request.args.get('item_type')
    item_id = request.args.get('item_id')
    user_id = request.args.get('user_id')

    if not user_id:
        return jsonify({'error': 'Missing user_id'}), 400

    try:
        query = """
            SELECT rating 
            FROM ratings 
            WHERE user_id = %s 
            AND item_type = %s 
            AND item_id = %s
        """
        
        result = db_utils(dbname='users_db', user='postgres').read_data(query, (user_id, item_type, item_id))
        print(result)
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

@app.route('/update-spotify-tokens', methods=['POST'])
def save_spotify_tokens():
    if 'user' not in session:
        return jsonify({"error": "Not authenticated"}), 401

    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    access_token = data.get('access_token')
    refresh_token = data.get('refresh_token')
    expires_in = data.get('expires_in')
    connected = data.get('connected')

    if 'user' in session and not 'spotify' in session['user']:
        session['user']['spotify'] = {}

    if connected:
        session['user']['spotify']['access_token'] = access_token
        session['user']['spotify']['refresh_token'] = refresh_token
        session['user']['spotify']['expires_in'] = expires_in
    session['user']['spotify']['connected'] = connected
    session.modified = True

    return jsonify({"success": "Save Spotify OAuth tokens"}), 200

@app.route('/get-spotify-status', methods=['GET'])
@cross_origin(supports_credentials=True)
def get_spotify_status():
    if 'user' in session and 'spotify' in session['user']:
        return jsonify({"connected": session['user']['spotify']['connected']}), 200
    return jsonify({"error": "Error getting Spotify status"}), 204

@app.route('/get-spotify-playlists', methods=['GET'])
@cross_origin(supports_credentials=True)
def get_spotify_playlists():
    if 'user' not in session or 'spotify' not in session['user'] or \
    not session['user']['spotify'].get('connected'):
        print("[Spotify] Not connected: user or spotify session missing or not connected.")
        return jsonify({"error": "Spotify not connected"}), 401

    access_token = session['user']['spotify'].get('access_token')
    if not access_token:
        print("[Spotify] No access token found in session.")
        return jsonify({"error": "No access token found"}), 401

    try:
        response = requests.get(
            'https://api.spotify.com/v1/me/playlists',
            headers={
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            },
            params={'limit': 50}
        )

        if response.status_code == 401:
            print(f"[Spotify] Token expired or invalid. Response: {response.text}")
            return jsonify({"error": "Spotify token expired"}), 401

        if response.status_code != 200:
            print(f"[Spotify] Unexpected error from Spotify API. Status: {response.status_code}, Response: {response.text}")
            return jsonify({"error": f"Spotify API error: {response.text}"}), 500

        return jsonify(response.json()), 200
    
    except Exception as e:
        print(f"Error fetching Spotify playlists: {e}")
        return jsonify({"error": f"Error fetching playlists: {str(e)}"}), 500

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
        else:
            return jsonify({'error': f'Invalid item_type: {item_type}'}), 400  # Error for unrecognized item_type

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
            if item_info:
                detailed_results.append({
                    "id": item_id,
                    "name": item_info[0].get(nameAlias, "Unknown"),  # Handle missing names
                    "rating": rating["rating"],
                    "created_at": created_at,  # Date without year
                })
        return jsonify(detailed_results), 200

    except Exception as e:
        print(f"Error fetching music list: {e}")
        return jsonify({'error': 'Server error'}), 500
    
# written by Matthew Stenvold
@app.route('/delete-user-rating', methods=['DELETE'])
def delete_user_rating():
    if 'user' not in session:
        return jsonify({'error': 'Not logged in'}), 401

    item_type = request.args.get('item_type')
    item_id = request.args.get('item_id')
    user_id = session['user']['id']

    # Define the delete query
    delete_query = """
        DELETE FROM ratings 
        WHERE user_id = %s AND item_type = %s AND item_id = %s
    """
    print("as")
    try:
        # Use mutate_data method to execute the delete query
        result = db_utils(dbname='users_db', user='postgres').mutate_data(delete_query, (user_id, item_type, item_id))

        if result is None:
            return jsonify({'message': 'Rating deleted successfully'}), 200
        else:
            return jsonify({'error': 'Rating not found or could not be deleted'}), 400

    except Exception as e:
        print(f"Error deleting rating: {e}")
        return jsonify({'error': 'Server error'}), 500

# Written by Matthew Stenvold
@app.route('/update-username', methods=['POST'])
def update_username():
    print("Session contents:", session)  # Debug print
    if 'user' not in session:
        return jsonify({'error': 'Not logged in'}), 401

    data = request.get_json()
    new_username = data.get('new_username')
    user_id = session['user']['id']

    if not new_username:
        return jsonify({'error': 'No username provided'}), 400

    try:
        db = db_utils(dbname='users_db', user='postgres')

        update_query = """
            UPDATE users
            SET username = %s
            WHERE id = %s
            RETURNING id;
        """
        result = db.mutate_data(update_query, (new_username, user_id))

        if not result:
            return jsonify({'error': 'User not found or username not updated'}), 404

        session['user']['username'] = new_username

        return jsonify({'success': True}), 200

    except psycopg.errors.UniqueViolation:
        return jsonify({'error': 'Username already taken'}), 409  # 409 = Conflict

    except Exception as e:
        print(f"Error updating username: {e}")
        return jsonify({'error': 'Server error'}), 500
    
# Written by Matthew Stenvold
@app.route('/update-user-pfp', methods=['POST'])
def update_user_pfp():
    if 'user' not in session:
        return jsonify({'error': 'Not logged in'}), 401

    user_id = session['user']['id']
    image_file = request.files.get('image')

    if not image_file:
        return jsonify({'error': 'No file uploaded'}), 400

    original_filename = secure_filename(image_file.filename)
    _, ext = os.path.splitext(original_filename)
    
    # Check if the uploaded file is an image and convert to PNG if not
    if ext.lower() not in ['.jpg', '.jpeg', '.png']:
        return jsonify({'error': 'Invalid file type. Only JPG, JPEG, and PNG are allowed.'}), 400

    # Force the file to be saved as .png
    filename = f"{user_id}profilepic.png"
    upload_path = os.path.join('static', 'pfp', filename)

    os.makedirs(os.path.dirname(upload_path), exist_ok=True)

    # If the image isn't already a PNG, convert it
    if ext.lower() != '.png':
        try:
            # Open the image using Pillow
            image = Image.open(image_file)
            # Save it as PNG
            image.save(upload_path, 'PNG')

        except Exception as e:
            return jsonify({'error': f'Error processing image: {str(e)}'}), 500
    else:
        # If it's already PNG, just save it
        image_file.save(upload_path)

    return jsonify({'success': True, 'filename': filename})

# Written by Matthew Stenvold
def get_profile_image_path(user_id):
    filename = f"{user_id}profilepic.png"
    image_path = os.path.join("static", "pfp", filename)

    if os.path.exists(image_path):
        
        return f"/static/pfp/{filename}"
        
    else:
        # If the image doesn't exist, send unknown user pfp
        return "/static/pfp/unknownPFP.png"
    
# Written by Matthew Stenvold
@app.route('/get-profile-image/<int:user_id>', methods=['GET'])
def get_profile_image(user_id):
    image_url = get_profile_image_path(user_id)
    print(image_url)
    return jsonify({'image_url': image_url})

# Written by Matthew Stenvold
@app.route('/get-bio/<int:user_id>', methods=['GET'])
def get_bio(user_id):
    try:
        db = db_utils(dbname='users_db', user='postgres')

        query = "SELECT bio FROM users WHERE id = %s;"
        result = db.read_data(query, (user_id,))

        if result:
            return jsonify({'bio': result[0]['bio']}), 200
        else:
            return jsonify({'error': 'User not found'}), 404

    except Exception as e:
        print(f"Error fetching bio: {e}")
        return jsonify({'error': 'Server error'}), 500

# Written by Matthew Stenvold
@app.route('/update-bio', methods=['POST'])
def update_bio():
    if 'user' not in session:
        return jsonify({'error': 'Not logged in'}), 401

    user_id = session['user']['id']
    new_bio = request.json.get('bio')

    # Validate bio length
    if new_bio and len(new_bio) > 500:
        return jsonify({'error': 'Bio cannot be longer than 500 characters'}), 400

    try:
        db = db_utils(dbname='users_db', user='postgres')

        update_query = """
            UPDATE users
            SET bio = %s
            WHERE id = %s
        """

        db.mutate_data(update_query, (new_bio, user_id))

        return jsonify({'success': True, 'bio': new_bio}), 200

    except Exception as e:
        print(f"Error updating bio: {e}")
        return jsonify({'error': 'Server error'}), 500
    
# Written by Matthew Stenvold
@app.route('/get-user-id/<string:username>', methods=['GET'])
def get_user_id(username):
    try:
        db = db_utils(dbname='users_db', user='postgres')
        query = "SELECT id FROM users WHERE username = %s;"
        result = db.read_data(query, (username,))
        
        if result:
            return jsonify({'id': result[0]['id']}), 200
        else:
            return jsonify({'error': 'User not found'}), 404
    except Exception as e:
        print(f"Error fetching user ID: {e}")
        return jsonify({'error': 'Server error'}), 500
    
# Written by Matthew Stenvold
@app.route('/user-rating-stats', methods=['GET'])
def get_user_rating_stats():
    user_id = request.args.get('user_id')

    if not user_id:
        return jsonify({'error': 'Missing user_id'}), 400

    try:
        query = """
            SELECT COUNT(*) AS total_ratings, 
                   COALESCE(AVG(rating), 0) AS average_rating
            FROM ratings
            WHERE user_id = %s
        """

        result = db_utils(dbname='users_db', user='postgres').read_data(query, (user_id,))
        stats = result[0] if result else {'total_ratings': 0, 'average_rating': 0}

        return jsonify(stats), 200

    except Exception as e:
        print(f"Error getting rating stats: {e}")
        return jsonify({'error': 'Server error'}), 500
    
# Written by Matthew Stenvold
@app.route('/user-recent-activity', methods=['GET'])
def get_recent_user_activity():
    user_id = request.args.get('user_id')
    limit = request.args.get('limit', 10)  # Default to 10 if no limit provided

    try:
        query = """
            SELECT
                'forum_thread' AS action_type,
                ft.created_at,
                ft.id AS action_id,
                'Created new thread titled "' || ft.title || '"' AS description,
                '/forum/thread/' || ft.id AS relevant_url
            FROM forum_threads ft
            WHERE ft.user_id = %s

            UNION ALL

            SELECT
                'forum_reply' AS action_type,
                fr.created_at,
                fr.id AS action_id,
                'Made a reply on the thread "' || ft.title || '"' AS description,
                '/forum/thread/' || fr.thread_id AS relevant_url
            FROM forum_replies fr
            JOIN forum_threads ft ON fr.thread_id = ft.id
            WHERE fr.user_id = %s

            UNION ALL

            SELECT
                'rating' AS action_type,
                r.created_at,
                r.id AS action_id,
                r.item_type || ' ' || r.item_id || ' ' || ROUND(r.rating)::INTEGER AS description,
                CASE
                    WHEN r.item_type = 'master' THEN '/master/' || r.item_id
                    WHEN r.item_type = 'artist' THEN '/artist/' || r.item_id
                    ELSE '/item/' || r.item_id
                END AS relevant_url
            FROM ratings r
            WHERE r.user_id = %s

            ORDER BY created_at DESC
            LIMIT %s;
        """

        result = db_utils(dbname='users_db', user='postgres').read_data(query, (user_id, user_id, user_id, limit))

        # Now process the description and replace item_id with title
        for activity in result:
            if activity['action_type'] == 'rating':
                # Extract item_type and item_id from description
                description_parts = activity['description'].split(' ')

                item_type = description_parts[0]
                item_id = description_parts[1]

                # Fetch the title based on item_type and item_id
                if item_type == 'master':
                    item_info = master.get_master(item_id)
                    title = item_info[0].get('title', 'Unknown Master')
                    action_type = "master_rating"
                elif item_type == 'artist':
                    item_info = artist.get_artist(item_id)
                    title = item_info[0].get('name', 'Unknown Artist')
                    action_type = "artist_rating"
                else:
                    title = 'Unknown Item'
                    action_type = "unknown_Rating"
                    print("Rating type unknown")

                # Add quotes around the title in the description
                activity['description'] = f"Rated \"{title}\" {description_parts[2]} stars"

                # Update the action_type to differentiate between master and artist
                activity['action_type'] = action_type

        return jsonify(result), 200
    except Exception as e:
        print(f"Error fetching recent activity: {e}")
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
        references = forum.get_thread_references(thread_id)
        
        # Retrieve the author profile image URL for the thread author
        thread_author_image_url = get_profile_image_path(thread_data[0]['author_id'])
        
        # Format the thread data
        formatted_thread = {
            "id": thread_data[0]['id'],
            "title": thread_data[0]['title'],
            "content": thread_data[0]['content'],
            "date": thread_data[0]['created_at'].strftime("%B %d, %Y") if isinstance(thread_data[0]['created_at'], datetime) else thread_data[0]['created_at'],
            "isEdited": thread_data[0].get('is_edited', False),
            "author": {
                "id": thread_data[0]['author_id'],
                "name": thread_data[0]['author_name'],
                "pfp": thread_author_image_url  # Add the profile image URL
            },
            "replies": [],
            "references": references
        }
        
        # Format the replies and include the author image URL for each reply author
        for reply in replies:
            reply_author_image_url = get_profile_image_path(reply['author_id'])
            formatted_reply = {
                "id": reply['id'],
                "content": reply['content'],
                "date": reply['created_at'].strftime("%B %d, %Y") if isinstance(reply['created_at'], datetime) else reply['created_at'],
                "isEdited": reply.get('is_edited', False),
                "isDeleted": reply.get('is_deleted', False),
                "parentId": reply['parent_id'],
                "author": {
                    "id": reply['author_id'],
                    "name": reply['author_name'],
                    "pfp": reply_author_image_url  # Add the profile image URL for the reply author
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
                reply_author_image_url = get_profile_image_path(new_reply['author_id'])
                formatted_reply = {
                    "id": new_reply['id'],
                    "content": new_reply['content'],
                    "date": new_reply['created_at'].strftime("%B %d, %Y") if isinstance(new_reply['created_at'], datetime) else new_reply['created_at'],
                    "isEdited": new_reply.get('is_edited', False),
                    "parentId": new_reply['parent_id'],
                    "author": {
                        "id": new_reply['author_id'],
                        "name": new_reply['author_name'],
                        "pfp": reply_author_image_url
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

@app.route('/admin/reports/resolve/<int:report_id>', methods=['PUT'])
@admin_required
def resolve_forum_report(report_id):
    try:
        data = request.get_json()
        is_resolved = data.get('isResolved')

        if is_resolved is not None:
            forum.resolve_report(report_id, is_resolved)

            return jsonify({"success": "Updated report as resolved"}), 200
        return jsonify({"error": "Database error resolving report"}), 500
    except Exception as e:
        print(f"Error fetching reports: {e}")
        return jsonify({"error": "Internal server error", "message": str(e)}), 500

@app.route('/admin/reports/delete-reply/<int:reply_id>', methods=['PUT'])
@admin_required
def delete_forum_report_reply(reply_id):
    try:
        data = request.get_json()
        is_deleted = data.get('isDeleted')

        if is_deleted is not None:
            forum.delete_report_reply(reply_id, is_deleted)

            return jsonify({"success": "Updated report reply as deleted"}), 200
        return jsonify({"error": "Database error deleting reply"}), 500
    except Exception as e:
        print(f"Error fetching reports: {e}")
        return jsonify({"error": "Internal server error", "message": str(e)}), 500

@app.route('/admin/reports/delete-thread/<int:thread_id>', methods=['PUT'])
@admin_required
def delete_forum_report_thread(thread_id):
    try:
        data = request.get_json()
        is_deleted = data.get('isDeleted')

        if is_deleted is not None:
            forum.delete_report_thread(thread_id, is_deleted)

            return jsonify({"success": "Updated report thread as deleted"}), 200
        return jsonify({"error": "Database error deleting thread"}), 500
    except Exception as e:
        print(f"Error fetching reports: {e}")
        return jsonify({"error": "Internal server error", "message": str(e)}), 500

@app.route('/forum/reference', methods=['POST'])
def add_forum_reference():
    if 'user' not in session:
        return jsonify({'error': 'Not logged in'}), 401

    if request.method == 'POST':
        data = request.get_json()
        item_type = data.get('item_type')
        item_id = data.get('item_id')
        reference_type = data.get('reference_type')
        reference_id = data.get('reference_id')
        reference_name = data.get('reference_name')

        if not all([item_type, item_id, reference_type, reference_id]):
            return jsonify({'error': 'Missing fields'}), 400

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
        return jsonify({'error': 'Not logged in'}), 401

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
    
@app.route('/reset-password', methods=['POST'])
def reset_password():
    data = request.get_json()
    token = data.get('token')
    new_password = data.get('password')
    
    if not token or not new_password:
        return jsonify({'error': 'Missing required fields'}), 400
        
    try:
        # Verify token and get user
        query = """
            SELECT user_id 
            FROM password_reset_tokens 
            WHERE token = %s AND expiry > CURRENT_TIMESTAMP;
        """
        result = db_utils(dbname='users_db', user='postgres').read_data(query, (token,))
        
        if not result:
            return jsonify({'error': 'Invalid or expired reset token'}), 400
            
        user_id = result[0]['user_id']
        
        # Update password
        hashed_password = generate_password_hash(new_password)
        update_query = """
            UPDATE users 
            SET password = %s 
            WHERE id = %s;
        """
        db_utils(dbname='users_db', user='postgres').mutate_data(update_query, (hashed_password, user_id))
        
        # Delete used token
        delete_query = "DELETE FROM password_reset_tokens WHERE token = %s;"
        db_utils(dbname='users_db', user='postgres').mutate_data(delete_query, (token,))
        
        return jsonify({'message': 'Password reset successful'}), 200
        
    except Exception as e:
        print(f"Password reset error: {str(e)}")
        return jsonify({'error': 'Failed to reset password'}), 500

@app.route('/user-top-genres', methods=['GET'])
def get_user_top_genres():
    user_id = request.args.get('user_id')
    
    if not user_id:
        return jsonify({'error': 'Missing user_id'}), 400
        
    try:
        # Get all master_ids rated by the user
        master_ids_query = """
            SELECT item_id
            FROM ratings
            WHERE user_id = %s AND item_type = 'master'
        """
        master_ids_result = db_utils(dbname='users_db', user='postgres').read_data(master_ids_query, (user_id,))
        
        if not master_ids_result:
            return jsonify([]), 200  # Return empty list if no ratings
            
        # Extract the master_ids
        master_ids = [r['item_id'] for r in master_ids_result]
        
        # Query for genres
        genres_query = """
            SELECT genre, COUNT(*) as count
            FROM master_genre
            WHERE master_id = ANY(%s::integer[])
            GROUP BY genre
            ORDER BY count DESC
            LIMIT 5;
        """
        genres_result = db_utils(dbname='discogs_db', user='postgres').read_data(genres_query, (master_ids,))
        
        # Calculate percentages
        total_count = sum(genre['count'] for genre in genres_result) if genres_result else 1
        
        top_genres = [
            {
                'name': genre['genre'],
                'percentage': round((genre['count'] / total_count) * 100)
            }
            for genre in genres_result
        ]
        
        return jsonify(top_genres), 200
        
    except Exception as e:
        print(f"Error fetching top genres: {e}")
        return jsonify({'error': 'Server error'}), 500
    
@app.route('/get-artist-stats', methods=['GET'])
def get_artist_stats():
    if request.method == 'GET':
        artist_id = int(request.args.get('artist_id'))
        
        try:
            # Get artist data
            artist_data = artist.get_artist(artist_id)
            if not artist_data:
                return jsonify({"error": "Artist not found"}), 404
                
            # Get discography
            discography = artist.get_discography(artist_id)
            if not discography:
                return jsonify({"error": "No discography found"}), 404
                
            # Sort discography by year to find most recent release
            sorted_discography = sorted(discography, key=lambda x: x.get('year', 0), reverse=True)
            recent_release = sorted_discography[0] if sorted_discography else None
            
            # Get the most popular album (based on number of versions)
            popular_album = max(discography, key=lambda x: len(release.get_all_versions_of_master(x['id'])))
            
            # Get the most popular track (based on number of releases)
            popular_track = None
            max_releases = 0
            for album in discography:
                tracks = release.get_release_tracklist(album['id'])
                for track in tracks:
                    track_releases = len(release.get_all_versions_of_master(album['id']))
                    if track_releases > max_releases:
                        max_releases = track_releases
                        popular_track = track
            
            # Get images for the releases
            recent_image = None
            popular_image = None
            if recent_release:
                recent_image = master.get_discogs_api_master(recent_release['id'], \
                                                             authenticate_discogs_API, \
                                                             discogs_client_instance)
            if popular_album:
                popular_image = master.get_discogs_api_master(popular_album['id'], \
                                                              authenticate_discogs_API, \
                                                              discogs_client_instance)
            
            response = {
                'top_album': {
                    'name': popular_album.get('title', 'Unknown'),
                    'year': popular_album.get('year', 'Unknown'),
                    'image_url': popular_image['images'][0]['uri'] if popular_image and 'images' in popular_image else '/images/UnknownSong.png'
                },
                'top_track': {
                    'name': popular_track.get('title', 'Unknown') if popular_track else 'Unknown',
                    'year': popular_album.get('year', 'Unknown'),
                    'image_url': popular_image['images'][0]['uri'] if popular_image and 'images' in popular_image else '/images/UnknownSong.png'
                },
                'recent_album': {
                    'name': recent_release.get('title', 'Unknown') if recent_release else 'Unknown',
                    'year': recent_release.get('year', 'Unknown') if recent_release else 'Unknown',
                    'image_url': recent_image['images'][0]['uri'] if recent_image and 'images' in recent_image else '/images/UnknownSong.png'
                }
            }
            
            return jsonify(response), 200
            
        except Exception as e:
            print(f"Error getting artist stats: {e}")
            return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    if authenticate_discogs_API:
        authenticate_discogs()
    app.run(host="0.0.0.0", port=5001, debug=True)

