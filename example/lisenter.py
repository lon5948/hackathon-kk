import websockets
import asyncio
import json
import re

serverURL = "ws://hackathon-kk.dasbd72.com"
clientId = "listener"

pattern = "([A-Z]+)\\*([0-9]+)"


def process(msg: str):
    content = json.loads(msg)
    ma = re.findall(pattern, content["message"])
    if ma is not None:
        print(content["name"])
        print(ma)


async def main():
    async for websocket in websockets.connect(f"{serverURL}/ws/chatroom/{clientId}"):
        try:
            async for msg in websocket:
                process(msg)
        except websockets.ConnectionClosed:
            continue


if __name__ == "__main__":
    asyncio.run(main())
