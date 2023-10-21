import asyncio
from websockets.sync.client import connect

def listen():
    with connect("ws://hackathon-kk.dasbd72.com/ws/chatroom/listener") as websocket:
        while True:
            message = websocket.recv()
            print(f"Received: {message}")

listen()