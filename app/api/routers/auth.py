from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import UserInDB
from app.schemas.auth import RefreshRequest, RegisterRequest, TokenResponse, LoginRequest
from app.db.database import get_db
from app.crud.crud_users import get_user_by_email
from app.crud.crud_auth import get_auth_user_by_refresh_token, get_auth_user_by_email, create_auth_user, update_refresh_token, logout_user
from app.core.security import create_access_token, verify_password, generate_refresh_token
from app.dependencies.auth import get_current_user

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
    if not user:
        raise HTTPException(status_code=400, detail="User not found")

    password_match = verify_password(login_data.password, user.auth.hashed_password)
    if not password_match:
        raise HTTPException(status_code=400, detail="Invalid email or password")
    
    access_token = create_access_token({"sub": str(user.id)})
    refresh_token, expires_at = generate_refresh_token().values()

    await update_refresh_token(db, user.id, refresh_token, expires_at)

    return TokenResponse(access_token=access_token, refresh_token=refresh_token)

@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    data: RefreshRequest,
    db: AsyncSession = Depends(get_db),
):
    auth = await get_auth_user_by_refresh_token(db, data.refresh_token)

    if not auth or auth.expires_at < datetime.now(timezone.utc):
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    new_access_token = create_access_token({"sub": str(auth.user_id)})
    new_refresh = generate_refresh_token()

    await update_refresh_token(
        db,
        auth.user_id,
        new_refresh["refresh_token"],
        new_refresh["expires_at"],
    )

    return TokenResponse(
        access_token=new_access_token,
        refresh_token=new_refresh["refresh_token"],
    )


@router.post("/logout")
async def logout(
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    await logout_user(db, current_user.id)
    return {"detail": "Logged out successfully"}

    