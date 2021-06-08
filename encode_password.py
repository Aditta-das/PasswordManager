from cryptography.fernet import Fernet
get_key = Fernet.generate_key()
cipher = Fernet(get_key)

def encrypt_me(password):
    pwd = cipher.encrypt(password)
    return pwd

def decrypt_me(bytepass):
    # encrypt = encrypt_me(bytepass)
    login_pwd = cipher.decrypt(bytepass)
    return login_pwd

print(decrypt_me(b'gAAAAABguyvnMxFMCE_mvKCVdVrHWZWzOhRRUkf8yKyvVc-rnW-uPVLlC7yKHKc_oOGnNArK4ahRAn9NABIenB3y5O5HJ9WgiQ=='))