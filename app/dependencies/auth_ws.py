from fastapi import WebSocket
from app.db.database import AsyncSessionLocal
from app.crud.crud_auth import get_user_from_token

async def get_current_user_ws(websocket: WebSocket):
    token = websocket.query_params.get("token")
    if not token:
        await websocket.close(code=1008)
        return None

    async with AsyncSessionLocal() as db:
        return await get_user_from_token(token, db)
