import secrets
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from datetime import datetime, timedelta, timezone
import jwt
from app.core.config import settings



ph = PasswordHasher()

def hash_password(password: str) -> str:
    return ph.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    """Verifies a plaintext password against a stored hash."""
    try:
        ph.verify(hashed_password, password)
        return True
    except VerifyMismatchError:
        # This exception is raised when the passwords don't match
        return False
    except Exception as e:
        # Handle other potential exceptions, such as an invalid hash format
        print(f"Error during verification: {e}")
        return False


def create_access_token(data: dict, expires_delta: int = None):
    to_encode = data.copy()
    
    # Use timezone-aware object for the current time in UTC
    expire = datetime.now(timezone.utc) + timedelta(minutes=expires_delta or settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

def decode_access_token(token: str) -> dict | None:
    try:
        return jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )
    except jwt.PyJWTError:
        return None

def generate_refresh_token(expires_delta: int = None):
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=expires_delta or settings.JWT_REFRESH_EXPIRE_MINUTES)
    return {
        "refresh_token": secrets.token_hex(32),
        "expires_at": expires_at
    }

