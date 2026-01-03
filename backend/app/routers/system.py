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
        "total_balance": user.total_balance,
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
            "total_balance": user.total_balance,
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
    id: int | None = await detect(imagefile)
    return {"id": id}

# ゲームコードごとのポイント設定
GAME_REWARD_POINTS = {
    "game_a": 50,
    "game_b": 100,
    "game_c": 150,
}

@router.post("/add-rewards", response_model=AddRewardResponse)
async def add_rewards(
    payload: AddRewardRequest,
    session: AsyncSession = Depends(get_async_session),
    api_key: str = Depends(verify_api_key)
):
    # 1. ユーザー取得
    result = await session.execute(select(User).filter(User.id == int(payload.user_id)))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # 2. ゲームコードに応じた獲得ポイントを決定
    reward_points = GAME_REWARD_POINTS.get(payload.game_code)
    if reward_points is None:
        raise HTTPException(status_code=400, detail="Unknown game code")

    # 3. 残高と累計ポイントを更新
    user.balance += reward_points
    user.total_balance += reward_points
    user.total_plays += 1

    await session.commit()
    await session.refresh(user)

    return AddRewardResponse(
        status="success",
        reward_added=reward_points,
        new_balance=user.balance,
        total_balance=user.total_balance,
    )