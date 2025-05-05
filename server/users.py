from db_utils import db_utils
from werkzeug.security import check_password_hash

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