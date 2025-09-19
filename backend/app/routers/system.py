from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Response, Cookie
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc, func
from pydantic import BaseModel

from db.session import get_async_session
from models.users import User
from core.verify_apikey import verify_api_key

router = APIRouter(prefix="/api", tags=["api"])

from schemas.system import UserIdRequest, AddBalanceRequest, AddRewardRequest, AddRewardResponse, RegisterRequest

from marker.detect import detect
from marker.marker_gen import generate_aruco_marker
import uuid


@router.get("/marker/{user_id}")
async def marker_endpoint(user_id: int):
    return generate_aruco_marker(user_id)

@router.get("/me")
async def get_or_init_me(
    response: Response,
    session: AsyncSession = Depends(get_async_session),
    session_id: str | None = Cookie(default=None)
):
    async def create_new_user() -> User:
        result = await session.execute(select(func.count()).select_from(User))
        count = result.scalar_one() or 0
        new_session_id = str(uuid.uuid4())

        new_user = User(
            session_id=new_session_id,
            balance=0,
            display_name=f"ゲスト{count + 1}"
        )
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)

        response.set_cookie("session_id", new_session_id, httponly=True)
        return new_user

    if session_id is None:
        user = await create_new_user()
    else:
        result = await session.execute(select(User).filter(User.session_id == session_id))
        user = result.scalars().first()
        if not user:
            user = await create_new_user()

    return {
        "user_id": user.id,
        "session_id": user.session_id,
        "display_name": user.display_name,
        "balance": user.balance,
        "total_plays": user.total_plays,
        "balance_resets_at": user.balance_resets_at,
        "last_active_at": user.last_active_at,
        "created_at": user.created_at
    }

    

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

@router.get("/marker/{user_id}")
async def marker_endpoint(user_id: int):
    return generate_aruco_marker(user_id)