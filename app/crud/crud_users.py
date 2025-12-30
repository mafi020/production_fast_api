from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.user import User

async def get_users(db: AsyncSession):
    users = await db.execute(select(User))
    return users.scalars().all()

async def get_user(db: AsyncSession, user_id: int):
    user = await db.execute(select(User).where(User.id == user_id))
    return user.scalar_one_or_none()

async def get_user_by_email(db: AsyncSession, email: str):
    user = await db.execute(select(User).where(User.email == email))
    return user.scalar_one_or_none()