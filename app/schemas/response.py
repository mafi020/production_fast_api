from typing import Generic, TypeVar, Optional
from pydantic import BaseModel
from pydantic.generics import GenericModel

T = TypeVar("T") 

class ResponseSchema(GenericModel, Generic[T]):
    status: int
    success: bool
    body: Optional[T] = None
    error: Optional[str | dict] = None
