import websockets
import asyncio
import signal

serverURL = "ws://hackathon-kk.dasbd72.com"
clientId = "listener"


async def main():
    async for websocket in websockets.connect(f"{serverURL}/ws/chatroom/{clientId}"):
        try:
            async for msg in websocket:
                print(msg)
        except websockets.ConnectionClosed:
            continue


if __name__ == "__main__":
    asyncio.run(main())
