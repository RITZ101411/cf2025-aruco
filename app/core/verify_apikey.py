from fastapi import HTTPException, Header
from dotenv import load_dotenv
import os

load_dotenv()

API_KEYS = os.getenv("API_KEYS", "").split(",")

def verify_api_key(authorization: str = Header(None)):
    if authorization is None:
        raise HTTPException(status_code=401, detail="API Key missing")
    if authorization not in API_KEYS:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    return authorization