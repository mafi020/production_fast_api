from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import UserInDB
from app.schemas.auth import RegisterRequest, TokenResponse, LoginRequest
from app.db.database import get_db
from app.crud.crud_users import get_user_by_email
from app.crud.crud_auth import create_auth_user, get_auth_user_by_email, update_refresh_token
from app.core.security import create_access_token, verify_password, generate_refresh_token

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserInDB)
async def register(register_data: RegisterRequest, db: AsyncSession = Depends(get_db)):
    existing = await get_user_by_email(db, register_data.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    user = await create_auth_user(db, register_data)
    return user

@router.post("/login", response_model=TokenResponse)
async def login(login_data: LoginRequest, db: AsyncSession = Depends(get_db)):
    user = await get_auth_user_by_email(db, login_data.email)
    if user:
        raise HTTPException(status_code=400, detail="User not found")
    
    password_match = verify_password(login_data.password, user.password)
    if not password_match:
        raise HTTPException(status_code=400, detail="Invalid email or password")
    
    access_token = create_access_token({"sub": user.id})
    refresh_token, expires_at = generate_refresh_token()

    await update_refresh_token(db, user.id, refresh_token, expires_at)

    return TokenResponse(access_token, refresh_token)

    