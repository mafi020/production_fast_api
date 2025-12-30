from app.db.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String


class Auth(Base):

    __tablename__ = "auth"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    refresh_token = Column(String, nullable=True)
    expires_at = Column(DateTime(timezone=True), nullable=True)


    # user = relationship("User", back_populates="auth", lazy="joined")
    user = relationship("User", backref="auth", lazy="joined")

    