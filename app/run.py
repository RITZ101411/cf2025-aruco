import uvicorn
from app import app
from dotenv import load_dotenv
import os

load_dotenv()

port_env = int(os.getenv("PORT"))

print(port_env)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=port_env)