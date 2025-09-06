from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel

from db.session import get_async_session
from models.users import User
from core.verify_apikey import verify_api_key

router = APIRouter(prefix="/system", tags=["system"])

from schemas.system import UserIdRequest, AddBalanceRequest

from marker.detect import detect

@router.get("/get-users")
async def get_users(
    session: AsyncSession = Depends(get_async_session),
    api_key: str = Depends(verify_api_key)
):
    result = await session.execute(select(User))
    users = result.scalars().all()
    return users

@router.post("/get-user")
async def get_user(
    payload: UserIdRequest,
    session: AsyncSession = Depends(get_async_session),
    api_key: str = Depends(verify_api_key)
):
    stmt = select(User).filter(User.id == payload.id)
    result = await session.execute(stmt)
    user = result.scalars().first()

    if user:
        return {
            "id": user.id,
            "user_id": user.user_id,
            "balance": str(user.balance),
            "reset_at": user.reset_at.isoformat() if user.reset_at else None,
            "created_at": user.created_at.isoformat(),
            "updated_at": user.updated_at.isoformat()
        }
    else:
        raise HTTPException(status_code=404, detail="User not found")

@router.post("/set-balance")
async def set_balance(
    payload: AddBalanceRequest,
    session: AsyncSession = Depends(get_async_session),
    api_key: str = Depends(verify_api_key)
):
    stmt = select(User).filter(User.id == payload.id)
    result = await session.execute(stmt)
    user = result.scalars().first()

    if user:
        user.balance = payload.value
        await session.commit()
        await session.refresh(user)
        return { "balance": str(user.balance) }
    else:
        raise HTTPException(status_code=404, detail="User not found")

@router.post("/reset-user")
async def reset_user(
    payload: UserIdRequest,
    session: AsyncSession = Depends(get_async_session),
    api_key: str = Depends(verify_api_key)
):
    stmt = select(User).filter(User.id == payload.id)
    result = await session.execute(stmt)
    user = result.scalars().first()

    if user:
        user.balance = 0
        await session.commit()
        await session.refresh(user)
        return {
            "message": f"User {user.user_id} has been reset.",
            "balance": str(user.balance),
        }
    else:
        raise HTTPException(status_code=404, detail="User not found")
    
@router.post("/get-user-marker")
async def get_user_marker(
    imagefile: UploadFile = File(...),
    session: AsyncSession = Depends(get_async_session),
    api_key: str = Depends(verify_api_key)
):
    id: int = await detect(imagefile)
    if id is []:
        raise ValueError({"No": "No"})
    return {"id": id}