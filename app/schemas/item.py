from pydantic import BaseModel, Field

class ItemBase(BaseModel):
    name: str = Field(min_length=1, max_length=255, strip_whitespace=True)
    description: str | None = None
    price: float

class ItemCreate(ItemBase):
    pass

class ItemInDB(ItemBase):
    id: int

    class Config:
        from_attributes = True
