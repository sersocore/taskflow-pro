from fastapi import APIRouter, WebSocket, Query, WebSocketDisconnect
from backend.app.services.websocket_manager import websocket_manager
from backend.app.api.dependencies import get_current_user_from_token
from uuid import UUID

router = APIRouter()

@router.websocket('/ws/notifications')
async def websocket_notifications(websocket: WebSocket, token: str = Query(...)):
    # Authentifier l'utilisateur via token
    user = await get_current_user_from_token(token)
    if not user:
        await websocket.close(code=1008)  # Policy Violation
        return

    user_id = user.id
    await websocket_manager.connect(websocket, user_id)

    try:
        while True:
            # Keep connection alive, no messages expected from client
            await websocket.receive_text()
    except WebSocketDisconnect:
        pass
    finally:
        await websocket_manager.disconnect(websocket, user_id)
