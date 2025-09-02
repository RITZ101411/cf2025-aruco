from pydantic import BaseModel

class AddBalanceRequest(BaseModel):
    id: int
    value: int