from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import UserInDB
from app.db.database import get_db
from app.crud.crud_users import get_users, get_user


router = APIRouter(prefix="/users", tags=["users"])

@router.get("/", response_model=list[UserInDB])
async def read_users(db: AsyncSession = Depends(get_db)):
    return await get_users(db)

@router.get("/{user_id}", response_model=UserInDB)
async def read_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    return user
