from zxcvbn import zxcvbn
import bcrypt


def check_strength(password):
    result = zxcvbn(password)
    score = result['score']
    if score == 3:
        response = "Mot de passe assez fort"
    elif score == 4:
        response = "Mot de passe très fort"
    else:
        response = "Mot de passe faible"
    return score, response

def hash_pw(password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed

def verify_password(pw_attempt:str, hashed):
    return bcrypt.checkpw(pw_attempt.encode(),hashed)
