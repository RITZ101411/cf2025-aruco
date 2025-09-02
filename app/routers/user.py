from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select
from pydantic import BaseModel

from config.database import get_async_session
from models.users import User

router = APIRouter(prefix="/users", tags=["user"])

class UserBalanceRequest(BaseModel):
    id: int

@router.post("/get-balance")
async def get_balance(
    payload: UserBalanceRequest,
    session: AsyncSession = Depends(get_async_session),
):
    id = payload.id
    stmt = select(User).filter(User.id == id)
    result = await session.execute(stmt)
    user = result.scalars().first()

    if user:
        return { "balance": str(user.balance) }
    else:
        raise HTTPException(status_code=404, detail="Id not found")
