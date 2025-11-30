from getpass import getpass
from operator import truediv

from database import PasswordManagerDB
from encryption import aes_encrypt
from password import check_strength, hash_pw
from util import User, Password


class Manager:
    def __init__(self):
        self.user: User | None = None
        self.password_db = PasswordManagerDB()

    def login(self, username, password):
        message, user = self.password_db.search_user(username, password)
        print(message)
        if user is not None:
            self.user = user
            return True
        else:
            return False

    def logout(self):
        self.user = None

    def create_user(self, username, password):
        self.password_db.create_user(username, hash_pw(password))

    def delete_user(self):
        self.password_db.delete_user(self.user.user_id)

    def add_password(self, label, password):
        key, ciphertext = aes_encrypt(password)
        password_id = self.password_db.insert_password(self.user.user_id, label, key, ciphertext)
        self.user.passwords.append(Password(password_id, label, key, ciphertext))

    def update_password(self, password_id: str, new_password: str):
        key, ciphertext = aes_encrypt(new_password)
        self.password_db.update_password(password_id, key, new_password)
        password = self.user.find_password_by_id_or_label(password_id)
        password.set_password(key, ciphertext)

    def delete_password(self, password):
        self.password_db.delete_password(password.password_id)
        self.user.passwords.remove(password)