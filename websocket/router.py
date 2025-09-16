import json
from datetime import datetime, timezone

from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from starlette.websockets import WebSocket, WebSocketDisconnect

#from main import connection_manager, redis_manager
from databases.database import get_db
from models import Message
from websocket.websocket_manager import ConnectionManager
from redis_manager import RedisManager
import uuid

ws_router = APIRouter()

redis_manager = RedisManager()
connection_manager = ConnectionManager()


@ws_router.post("/room/create")
async def create_room():

    room_id = str(uuid.uuid4())
    return {"room_id": room_id}


@ws_router.websocket("/ws/chat/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: str, db: Session = Depends(get_db)):

    await websocket.accept()
    init_data = await websocket.receive_text()
    init_json = json.loads(init_data)
    username = init_json.get("username", "Anonymous")

    await connection_manager.connect(websocket, room_id)

    try:
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)

            timestamp = datetime.now(timezone.utc)
            message_data.update({
                "timestamp": timestamp.isoformat(),
                "room_id": room_id,
                "username": username
            })


            db_message = Message(
                username=username,
                text=message_data["text"],
                timestamp=timestamp
            )
            db.add(db_message)
            db.commit()
            db.refresh(db_message)

            message_data["id"] = db_message.id

            await redis_manager.save_message(room_id, message_data)

            await connection_manager.broadcast(json.dumps(message_data), room_id)

    except WebSocketDisconnect:
        connection_manager.disconnect(websocket, room_id)
        await connection_manager.broadcast(json.dumps({
            "username": "System",
            "text": f"{username} покинул комнату",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }), room_id)