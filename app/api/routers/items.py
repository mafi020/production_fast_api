from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.schemas.item import ItemCreate, ItemInDB
from app.crud.crud_items import create_item, get_items, get_item
from app.dependencies.auth import get_current_user

router = APIRouter(
    prefix="/items", 
    tags=["items"], 
    dependencies=[Depends(get_current_user)],
)

@router.post("/", response_model=ItemInDB)
async def create_new_item(item: ItemCreate, db: AsyncSession = Depends(get_db)):
    return await create_item(db, item)

@router.get("/", response_model=list[ItemInDB])
async def read_all_items(db: AsyncSession = Depends(get_db)):
    return await get_items(db)

@router.get("/{item_id}", response_model=ItemInDB)
async def read_item(item_id: int, db: AsyncSession = Depends(get_db)):
    item = await get_item(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item
