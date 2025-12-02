import sqlite3 as sq
import uuid

from password import verify_password
from util import User, Password


class PasswordManagerDB:
    def __init__(self):
        self.conn = sq.connect("passwords.db")
        self.cursor = self.conn.cursor()

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS passwords (
                id TEXT PRIMARY KEY,
                label TEXT NOT NULL UNIQUE,
                login TEXT,
                key TEXT NOT NULL,
                password TEXT NOT NULL,
                user_id TEXT NOT NULL,
                FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        ''')

        self.conn.commit()

    def __del__(self):
        self.conn.close()

    def create_user(self, username, password):
        user_id = str(uuid.uuid4())
        self.cursor.execute('''
            INSERT INTO users(id, username, password) VALUES (?, ?, ?)
        ''', (user_id, username, password))
        self.conn.commit()

    def search_user(self, username, password):
        self.cursor.execute('''
            SELECT id, username, password FROM users WHERE username = ?
        ''', (username,))

        user = self.cursor.fetchone()

        if user is not None and verify_password(password, user[-1]):
            passwords = self.get_passwords(user[0])
            return "Connexion réussie" ,User(user[0], user[1], passwords)
        else:
            return "Utilisateur non existant ou mot de passe incorrect ", None


    def get_passwords(self, user_id):
        self.cursor.execute('''
            SELECT id, label, key, password, login FROM passwords WHERE user_id = ?
        ''', (user_id,))

        result = self.cursor.fetchall()

        if len(result) == 0:
            return []
        passwords: list[Password] = [Password(*password) for password in result]
        return passwords

    def insert_password(self, user_id, label ,key, password, login=""):
        password_id = str(uuid.uuid4())
        self.cursor.execute('''
            INSERT INTO passwords(id, label, key, password, user_id, login) VALUES (?, ?, ?, ?, ?, ?)
        ''', (password_id, label, key, password, user_id, login))
        self.conn.commit()
        return password_id

    def update_password(self, password_id, new_key ,new_password):
        self.cursor.execute('''
            UPDATE passwords SET password = ?, key = ? WHERE id = ?
        ''', (new_password, new_key, password_id))
        self.conn.commit()

    def delete_password(self, password_id):
        self.cursor.execute('''
            DELETE FROM passwords WHERE id = ?
        ''', (password_id,))
        self.conn.commit()

    def delete_user(self, user_id):
        self.cursor.execute("""
            DELETE FROM users WHERE id = ?
        """, (user_id,))
        self.conn.commit()
