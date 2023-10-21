import asyncio
import time

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from routers.manager import connectionManager

router = APIRouter()


@router.websocket("/ws/chatroom/{client_id}")
async def ws_symbol_events(websocket: WebSocket, client_id: str):
    await connectionManager.connect(websocket)

    if client_id != "listener":
        await connectionManager.broadcast_json(
            {
                "timestamp": int(time.time() * 1000),
                "event-type": "system",
                "client-id": client_id,
                "name": "System",
                "message": f"Client #{client_id} joined the chat",
            }
        )
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
                await connectionManager.broadcast(data)

        except WebSocketDisconnect:
            connectionManager.disconnect(websocket)
            await connectionManager.broadcast_json(
                {
                    "timestamp": int(time.time() * 1000),
                    "event-type": "system",
                    "client-id": client_id,
                    "name": "System",
                    "message": f"Client #{client_id} left the chat",
                }
            )
    else:
        try:
            while True:
                # receive client message or continue if timeout
                try:
                    data = await asyncio.wait_for(
                        websocket.receive_text(), timeout=1
                    )
                except asyncio.TimeoutError:
                    continue

        except WebSocketDisconnect:
            connectionManager.disconnect(websocket)
