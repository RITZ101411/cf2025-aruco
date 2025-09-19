from sqlalchemy import Column, Integer, String, DECIMAL, DateTime, func
from db.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)   
    session_id = Column(String(64), unique=True, nullable=False) 
    display_name = Column(String(50), nullable=True)
    balance = Column(Integer, nullable=False, default=0)
    total_plays = Column(Integer, nullable=False, default=0)
    total_balance = Column(Integer, nullable=False, default=0)
    balance_resets_at = Column(DateTime, nullable=True)
    last_active_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    created_at = Column(DateTime, server_default=func.now())
