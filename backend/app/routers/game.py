from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel

from db.session import get_async_session
from models.users import User
from core.verify_apikey import verify_api_key

router = APIRouter(prefix="/games", tags=["game"])

from schemas.game import AddBalanceRequest

@router.post("/add-balance")
async def add_balance(
    payload: AddBalanceRequest,
    session: AsyncSession = Depends(get_async_session),
    api_key: str = Depends(verify_api_key)
):
    stmt = select(User).filter(User.id == payload.id)
    result = await session.execute(stmt)
    user = result.scalars().first()

    if user:
        user.balance += payload.value
        await session.commit()
        await session.refresh(user)
        return { "balance": str(user.balance) }
    else:
        raise HTTPException(status_code=404, detail="User not found")

@router.post("/remove-balance")
async def remove_balance(
    payload: AddBalanceRequest,
    session: AsyncSession = Depends(get_async_session),
    api_key: str = Depends(verify_api_key)
):
    stmt = select(User).filter(User.id == payload.id)
    result = await session.execute(stmt)
    user = result.scalars().first()

    if user:
        user.balance -= payload.value
        await session.commit()
        await session.refresh(user)
        return { "balance": str(user.balance) }
    else:
        raise HTTPException(status_code=404, detail="User not found")
