


from typing import Dict, List
from starlette.websockets import WebSocket

class ConnectionManager:
    def __init__(self):
        # Словарь: {room_id: [websockets]}
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, room_id: str):
        if room_id not in self.active_connections:
            self.active_connections[room_id] = []
        self.active_connections[room_id].append(websocket)

    def disconnect(self, websocket: WebSocket, room_id: str):
        if room_id in self.active_connections:
            self.active_connections[room_id].remove(websocket)
            if not self.active_connections[room_id]:
                del self.active_connections[room_id]

    async def broadcast(self, message: str, room_id: str):

        if room_id in self.active_connections:
            for connection in self.active_connections[room_id]:
                await connection.send_text(message)