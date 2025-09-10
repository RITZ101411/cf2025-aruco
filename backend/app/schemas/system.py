from pydantic import BaseModel

class UserIdRequest(BaseModel):
    id: int

class AddBalanceRequest(BaseModel):
    id: int
    value: int

class AddRewardRequest(BaseModel):
    user_id: str
    game_code: str
    score: int
    clear_time: float

class AddRewardResponse(BaseModel):
    status: str
    reward_added: int
    new_balance: int