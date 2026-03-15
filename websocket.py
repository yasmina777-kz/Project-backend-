from fastapi import APIRouter, WebSocket
from starlette.websockets import WebSocketDisconnect

router = APIRouter()

connections = {}

@router.websocket("/ws/{chat_id}")
async def websocket_endpoint(websocket: WebSocket, chat_id: int):
    await websocket.accept()

    connections.setdefault(chat_id, []).append(websocket)

    try:
        while True:
            data = await websocket.receive_text()


            for conn in connections[chat_id]:
                await conn.send_text(data)

    except WebSocketDisconnect:
        connections[chat_id].remove(websocket)