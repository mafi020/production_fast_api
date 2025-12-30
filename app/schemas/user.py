from pydantic import BaseModel, EmailStr, Field

class UserBase(BaseModel):
    first_name: str = Field(min_length=1, max_length=255, strip_whitespace=True)
    last_name: str = Field(min_length=1, max_length=255, strip_whitespace=True)
    email: EmailStr = Field(min_length=1, max_length=255, strip_whitespace=True)

class UserInDB(UserBase):
    id: int

    class Config():
        from_attributes = True    