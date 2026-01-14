from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import json

from app.core.ws_manager import ws_manager
from app.core.ws_event_bus import ws_event_bus
from app.dependencies.auth_ws import get_current_user_ws

router = APIRouter()


@router.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    # 1️⃣ Authenticate during handshake
    user = await get_current_user_ws(ws)
    if not user:
        return  # socket already closed inside dependency

    client_id = str(user.id)

    # 2️⃣ Register connection
    await ws_manager.connect(client_id, ws)
    print(f"WebSocket connected: user={client_id}")

    try:
        while True:
            raw = await ws.receive_text()
            event = json.loads(raw)

            # Expected envelope:
            # {
            #   "action": "subscribe|unsubscribe|emit",
            #   "topic": "orders.123",
            #   "data": {...}
            # }

            await ws_event_bus.emit(
                event=event,
                source=client_id,
            )

    except WebSocketDisconnect:
        print(f"WebSocket disconnected: user={client_id}")
        ws_manager.disconnect(client_id)

    except Exception as e:
        print(f"WebSocket error ({client_id}): {e}")
        ws_manager.disconnect(client_id)
        await ws.close(code=1011)
