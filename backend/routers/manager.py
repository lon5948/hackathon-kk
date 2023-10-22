from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, WebSocket] = {}

    async def connect(self, client_id: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[client_id] = websocket

    def disconnect(self, client_id: str):
        del self.active_connections[client_id]

    async def send_to(self, message: str, dest_id: str):
        await self.active_connections[dest_id].send_text(message)

    async def send_json_to(self, message: dict, dest_id: str):
        await self.active_connections[dest_id].send_json(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await self.active_connections[connection].send_text(message)

    async def broadcast_json(self, message: dict):
        for connection in self.active_connections:
            await self.active_connections[connection].send_json(message)


connectionManager = ConnectionManager()
