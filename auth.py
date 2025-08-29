from datetime import datetime, timedelta, timezone
import secrets
from typing import Optional
from jwt import api_jwt
import bcrypt



SECRET_KEY = "super-secret-key"
ALGORITHM = "HS256"




def create_jwt(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    now_utc = datetime.now(timezone.utc)
    expire = now_utc + (expires_delta or timedelta(minutes=30))
    to_encode.update({
        "exp": expire,
        "iat": now_utc,
        "jti": secrets.token_urlsafe()
    })
    return api_jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_jwt(token: str):
    try:
        return api_jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except Exception:
        return None

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed.encode('utf-8'))