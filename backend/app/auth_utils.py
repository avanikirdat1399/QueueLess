from passlib.hash import pbkdf2_sha256


# Convert password into a secure hash
def hash_password(password):
    return pbkdf2_sha256.hash(password)


# Verify entered password against stored hash
def verify_password(plain_password, hashed_password):
    return pbkdf2_sha256.verify(
        plain_password,
        hashed_password
    )