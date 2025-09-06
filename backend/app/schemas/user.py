from pydantic import BaseModel

class UserBalanceRequest(BaseModel):
    id: int