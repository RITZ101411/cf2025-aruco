from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.game_reward import GameReward

async def get_reward_points(session: AsyncSession, game_code: str) -> int | None:
    result = await session.execute(select(GameReward).filter(GameReward.game_code == game_code))
    reward = result.scalars().first()
    if reward:
        return reward.reward_points
    return None
