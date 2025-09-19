from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Response, Cookie
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from pydantic import BaseModel

from db.session import get_async_session
from models.users import User
from core.verify_apikey import verify_api_key

router = APIRouter(prefix="/api", tags=["api"])

from schemas.system import UserIdRequest, AddBalanceRequest, AddRewardRequest, AddRewardResponse, RegisterRequest

from marker.detect import detect
import uuid

@router.get("/me")
async def get_me(session: AsyncSession = Depends(get_async_session), session_id: str | None = Cookie(default=None)):
    if session_id is None:
        raise HTTPException(status_code=401, detail="No session_id")
    result = await session.execute(select(User).filter(User.session_id == session_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        "session_id": user.session_id,
        "display_name": user.display_name,
        "balance": user.balance,
        "total_plays": user.total_plays,
        "balance_resets_at": user.balance_resets_at,
        "last_active_at": user.last_active_at,
        "created_at": user.created_at
    }

@router.get("/init")
async def init(
    response: Response,
    session: AsyncSession = Depends(get_async_session),
    session_id: str | None = Cookie(default=None)
):
    if session_id is None:
        new_session_id = str(uuid.uuid4())

        new_user = User(session_id=new_session_id, balance=0)
        session.add(new_user)
        await session.commit()
        response.set_cookie("session_id", new_session_id, httponly=True)
        return {"message": "new user created", "session_id": new_session_id}
    else:
        return {"message": "user already exists", "session_id": session_id}

@router.get("/get-users")
async def get_users(
    session: AsyncSession = Depends(get_async_session),
):
    result = await session.execute(
        select(User).order_by(desc(User.balance))
    )
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
            "session_id": user.session_id,
            "display_name": user.display_name,
            "balance": str(user.balance),
            "total_plays": user.total_plays,
            "balance_resets_at": user.balance_resets_at.isoformat() if user.balance_resets_at else None,
            "last_active_at": user.last_active_at.isoformat(),
            "created_at": user.created_at.isoformat()
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

    
@router.post("/get-user-marker")
async def get_user_marker(
    imagefile: UploadFile = File(...),
    session: AsyncSession = Depends(get_async_session),
    api_key: str = Depends(verify_api_key)
):
    id: int = await detect(imagefile)
    if not id:
        raise ValueError({"No": "No"})
    return {"id": id}

@router.post("/add-rewards", response_model=AddRewardResponse)
async def add_rewards(
    payload: AddRewardRequest,
    api_key: str = Depends(verify_api_key)
    ):

    print("Received reward request:", payload)

    # 仮の固定レスポンス
    return AddRewardResponse(
        status="success",
        reward_added=50,
        new_balance=150,
    )