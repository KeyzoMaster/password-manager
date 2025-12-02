import secrets
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

def aes_encrypt(message):
    key = secrets.token_bytes(32)
    nonce = secrets.token_bytes(12)
    aes = AESGCM(key)
    ciphertext = nonce + aes.encrypt(nonce, message.encode(),None)
    return key.hex(), ciphertext.hex()

def aes_decrypt(key, message):
    ciphertext = bytes.fromhex(message)
    aes = AESGCM(bytes.fromhex(key))
    plaintext = aes.decrypt(ciphertext[:12], ciphertext[12:], None)
    return plaintext.decode()
