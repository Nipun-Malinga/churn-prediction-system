import bcrypt


def encrypt_password(password):
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def validate_password(password, hashed_password):
    try:
        return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))
    except ValueError as ex:
        raise ValueError(f"Invalid Value Detected during encoding: {ex}") from ex
