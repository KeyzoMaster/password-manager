from encryption import aes_decrypt

class User:
    def __init__(self, user_id, username, passwords):
        self.user_id = user_id
        self.username = username
        self.passwords: list[Password] = passwords

    def find_password_by_id_or_label(self, password_id_or_label):
        for password in self.passwords:
            if password.password_id == password_id_or_label or password.label == password_id_or_label:
                return password
        return None

class Password:
    def __init__(self, password_id: str, label: str, key: str, password: str, login: str = ""):
        self.password_id = password_id
        self.label = label
        self.login = login
        self._key = key
        self._password = password

    def get_password(self):
        return aes_decrypt(self._key, self._password)

    def set_password(self, key, password):
        self._key = key
        self._password = password