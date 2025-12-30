import secrets
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from datetime import datetime, timedelta, timezone
import jwt
from app.core import security


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
    expire = datetime.now(timezone.utc) + timedelta(minutes=expires_delta or security.jwt_expire_minutes)
    
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, security.jwt_secret_key, algorithm=security.jwt_algorithm)

def generate_refresh_token(expires_delta: int = None):
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=expires_delta or security.refresh_expire_minutes)
    return {
        "refresh_token": secrets.token_hex(32),
        "expires_at": expires_at
    }

