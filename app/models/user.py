from app.db.database import Base
from sqlalchemy import Column, Integer, String

class User(Base):

    __tablename__ = "users"

    id = Column(Integer, index=True, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)


    
