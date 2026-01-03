from sqlalchemy import Column, Integer, String
from db.base import Base

class GameReward(Base):
    __tablename__ = "game_rewards"

    id = Column(Integer, primary_key=True, index=True)
    game_code = Column(String(50), unique=True, nullable=False)
    reward_points = Column(Integer, nullable=False)