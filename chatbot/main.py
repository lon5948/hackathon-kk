import asyncio
import json
import os
import re

import websockets
from dotenv import load_dotenv

load_dotenv()

WS_API_URL = os.getenv("WS_API_URL")
clientId = "chatbot"

pattern = "([A-Z]+)\\*([0-9]+)"


def process(msg: str):
    content = json.loads(msg)
    ma = re.findall(pattern, content["message"])
    if ma:
        print(content["name"], ma)


async def ws_thread():
    async for websocket in websockets.connect(
        f"{WS_API_URL}/chatroom/{clientId}"
    ):
        try:
            async for msg in websocket:
                process(msg)
        except websockets.ConnectionClosed:
            continue


async def run_listener():
    task1 = asyncio.create_task(ws_thread())
    print("chatbot is up")
    await asyncio.gather(task1)


if __name__ == "__main__":
    asyncio.run(run_listener())
