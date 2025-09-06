from sqlalchemy import Column, Integer, String, DECIMAL, DateTime, func
from db.base import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(255), unique=True, nullable=False)
    balance = Column(DECIMAL(10, 2), nullable=False, default=0.00)
    reset_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())