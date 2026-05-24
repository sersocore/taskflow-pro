import asyncio
from typing import Dict, Set
from fastapi import WebSocket
from uuid import UUID
from backend.app.api.dependencies import get_current_user_from_token

class WebSocketManager:
    def __init__(self):
        # user_id (UUID) -> set of WebSocket connections
        self.active_connections: Dict[UUID, Set[WebSocket]] = {}
        self.lock = asyncio.Lock()

    async def connect(self, websocket: WebSocket, user_id: UUID):
        await websocket.accept()
        async with self.lock:
            conns = self.active_connections.get(user_id, set())
            conns.add(websocket)
            self.active_connections[user_id] = conns

    async def disconnect(self, websocket: WebSocket, user_id: UUID):
        async with self.lock:
            conns = self.active_connections.get(user_id)
            if conns and websocket in conns:
                conns.remove(websocket)
                if not conns:
                    del self.active_connections[user_id]

    async def send_personal_message(self, websocket: WebSocket, message: dict):
        await websocket.send_json(message)

    async def broadcast_to_user(self, user_id: UUID, message: dict):
        async with self.lock:
            conns = self.active_connections.get(user_id, set()).copy()
        for connection in conns:
            try:
                await connection.send_json(message)
            except Exception:
                # Ignore send errors, connection might be closed
                pass

websocket_manager = WebSocketManager()
