from datetime import datetime
from typing import Optional
from sqlalchemy import select, update
from app.schemas.auth import RegisterRequest
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.models.auth import Auth
from app.core import security

async def get_auth_user_by_id(db: AsyncSession, user_id: int):
    user = await db.execute(select(User).where(Auth.user_id == user_id))
    return user.scalar_one_or_none()

async def get_auth_user_by_email(db: AsyncSession, email: str):
    user = await db.execute(select(Auth).where(Auth.email == email))
    return user.scalar_one_or_none()

async def get_user_by_refresh_token(db: AsyncSession, refresh_token: str):
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
    