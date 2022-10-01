import hashlib
import time
import jwt
from app.config import SECRET_KEY, ALGORITHM, JWT_KEY


def get_password_hash(password: str) -> str:
    return hashlib.sha256(f'{SECRET_KEY}{password}'.encode('utf-8')).hexdigest()


def get_session_token(user_id: str) -> str:
    payload = {
        "user_id": user_id,
        "time": time.time()
    }
    return jwt.encode(payload, key=JWT_KEY, algorithm=ALGORITHM)
