from datetime import datetime
from typing import Optional
from fastapi import HTTPException
from sqlalchemy import select, update
from sqlalchemy.orm import selectinload
from app.schemas.auth import RegisterRequest
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.models.auth import Auth
from app.core import security

async def get_auth_user_by_id(db: AsyncSession, user_id: int):
    user = await db.execute(select(Auth).where(Auth.user_id == user_id))
    return user.scalar_one_or_none()

async def get_auth_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(
        select(User)
        .options(selectinload(User.auth))
        .where(User.email == email)
    )
    return result.scalar_one_or_none()

async def get_auth_user_by_refresh_token(db: AsyncSession, refresh_token: str):
    user = await db.execute(select(Auth).where(Auth.refresh_token == refresh_token))
    return user.scalar_one_or_none()

async def create_auth_user(db: AsyncSession, register_data: RegisterRequest):
    user = User(first_name=register_data.first_name, last_name=register_data.last_name, email=register_data.email)
    db.add(user)
    # to get user.id before commit
    await db.flush()

    hashed_password = security.hash_password(register_data.password)
    auth = Auth(user_id=user.id, hashed_password=hashed_password)
    db.add(auth)

    await db.commit()
    await db.refresh(user)
    return user

async def update_refresh_token(
    db: AsyncSession,
    user_id: int,
    refresh_token: str,
    expires_at: datetime
) -> Optional[Auth]:
    # Build the update query
    stmt = (
        update(Auth)
        .where(Auth.user_id == user_id)
        .values(
            refresh_token=refresh_token,
            expires_at=expires_at,
        )
        .returning(Auth)  # 👈 return the updated record
    )

    # Execute and commit
    result = await db.execute(stmt)
    await db.commit()

    # Return the updated Auth object
    updated_auth = result.scalar_one_or_none()
    return updated_auth

async def logout_user(db: AsyncSession, user_id: int) -> Optional[Auth]:
    # Invalidate the refresh token
    stmt = (
        update(Auth)
        .where(Auth.user_id == user_id)
        .values(
            refresh_token=None,
            expires_at=None,
        )
        .returning(Auth)
    )

    result = await db.execute(stmt)
    await db.commit()

    return result.scalar_one_or_none()

async def get_user_from_token(token: str, db: AsyncSession):
    payload = security.decode_access_token(token)

    if payload is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token",
        )

    sub = payload.get("sub")
    if sub is None:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    try:
        user_id = int(sub)
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid token subject")

    user = await get_auth_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")

    return user

    