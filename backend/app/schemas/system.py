from pydantic import BaseModel

class UserIdRequest(BaseModel):
    id: int

class AddBalanceRequest(BaseModel):
    id: int
    value: int