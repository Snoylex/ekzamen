from flask_login import UserMixin
from app import mysql

class User(UserMixin):
    def __init__(self, id, username, email, is_admin=False):
        self.id = id
        self.username = username
        self.email = email
        self.is_admin = bool(is_admin)

def load_user(user_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, username, email, is_admin FROM users WHERE id = %s", (user_id,))
    user_data = cur.fetchone()
    cur.close()
    if user_data:
        return User(user_data['id'], user_data['username'], user_data['email'], user_data['is_admin'])
    return None