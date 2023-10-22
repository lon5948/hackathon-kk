import asyncio
import json
import time
import logging

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from routers.manager import connectionManager

router = APIRouter()


@router.websocket("/ws/chatroom/{client_id}")
async def ws_symbol_events(websocket: WebSocket, client_id: str):
    await connectionManager.connect(client_id, websocket)

    if client_id == "listener":
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
            connectionManager.disconnect(client_id)
    elif client_id == "chatbot":
        try:
            while True:
                # receive client message or continue if timeout
                try:
                    data = await asyncio.wait_for(
                        websocket.receive_text(), timeout=1
                    )
                except asyncio.TimeoutError:
                    continue
                
                parsed_data = json.loads(data)
                if "dest-id" in parsed_data:
                    dest_id = parsed_data["dest-id"]
                    await connectionManager.send_to(data, dest_id)
                else:
                    await connectionManager.broadcast(data)

        except WebSocketDisconnect:
            connectionManager.disconnect(client_id)
    else:
        try:
            data = await asyncio.wait_for(
                websocket.receive_text(), timeout=1
            )
            parsed_data = json.loads(data)

            if parsed_data["event-type"] != "join" or parsed_data[
                "client-id"
            ] != client_id:
                raise Exception("Invalid join request")

            name = parsed_data["name"]

        except Exception as e:
            logging.error(f"Client id {client_id} failed to connect: {e}")
            connectionManager.disconnect(client_id)

        await connectionManager.broadcast_json(
            {
                "timestamp": int(time.time() * 1000),
                "event-type": "system",
                "client-id": client_id,
                "name": "System",
                "message": f"{name} joined the chat",
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
            connectionManager.disconnect(client_id)
            await connectionManager.broadcast_json(
                {
                    "timestamp": int(time.time() * 1000),
                    "event-type": "system",
                    "client-id": client_id,
                    "name": "System",
                    "message": f"{name} left the chat",
                }
            )
