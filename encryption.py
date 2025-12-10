import secrets
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from decouple import config

KEY =  bytes.fromhex(config('SECRET_KEY'))
aes = AESGCM(KEY)

def aes_encrypt(message):
    nonce = secrets.token_bytes(12)
    ciphertext = nonce + aes.encrypt(nonce, message.encode(),None)
    return ciphertext.hex()

def aes_decrypt(message):
    ciphertext = bytes.fromhex(message)
    plaintext = aes.decrypt(ciphertext[:12], ciphertext[12:], None)
    return plaintext.decode()
