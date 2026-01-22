from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()

def generate_password_hash(password: str):
    return password_hash.hash(password)

def verify_password(password: str, hashed_password: str):
    return password_hash.verify(password, hashed_password)