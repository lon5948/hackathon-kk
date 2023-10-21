import asyncio

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import time

from routers.manager import consoleManager

router = APIRouter()


@router.websocket("/ws/chatroom/{client_id}")
async def ws_symbol_events(websocket: WebSocket, client_id: str):
    await consoleManager.connect(websocket)
    await consoleManager.broadcast_json({
        "timestamp": int(time.time() * 1000),
        "event-type": "system",
        "client-id": client_id,
        "email": "",
        "message": f"Client #{client_id} joined the chat",
    })
    try:
        while True:
            # receive client message or continue if timeout
            try:
                data = await asyncio.wait_for(
                    websocket.receive_text(), timeout=1
                )
            except asyncio.TimeoutError:
                continue

            # send message to all clients
            await consoleManager.broadcast(data)

    except WebSocketDisconnect:
        consoleManager.disconnect(websocket)
        await consoleManager.broadcast_json({
            "timestamp": int(time.time() * 1000),
            "event-type": "system",
            "client-id": client_id,
            "email": "",
            "message": f"Client #{client_id} left the chat",
        })
