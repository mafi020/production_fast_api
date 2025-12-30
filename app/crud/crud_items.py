from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.item import Item
from app.schemas.item import ItemCreate, ItemInDB

async def create_item(db: AsyncSession, item: ItemCreate) -> ItemInDB:
    db_item = Item(**item.model_dump())
    db.add(db_item)
    await db.commit()
    await db.refresh(db_item)
    return db_item

async def get_items(db: AsyncSession):
    result = await db.execute(select(Item))
    return result.scalars().all()

async def get_item(db: AsyncSession, item_id: int):
    result = await db.execute(select(Item).where(Item.id == item_id))
    return result.scalar_one_or_none()
