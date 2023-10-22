import asyncio
import json
import os
import re
import time

import openai
import websockets
from dotenv import load_dotenv

load_dotenv()

openai.organization = "org-eNSouZjGbZlSWgbQFUM09Jon"
openai.api_key = os.getenv("OPENAI_API_KEY")
model_id = "gpt-3.5-turbo"
model_list = openai.Model.list()

messages = []
messages.append(
    {
        "role": "assistant",
        "content": "I am the chatbot for selling clothes, you can ask me anything about my products.",
    }
)


def chatbot(text):
    if text:
        messages.append({"role": "user", "content": text})
        chat = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=messages
        )
        reply = chat.choices[0].message.content
        messages.append({"role": "assistant", "content": reply})
        return reply


# while True:
#     text = input("You: ")
#     if text == "exit":
#         break
#     else:
#         print("Bot:", chatbot(text), "\n")
# exit(0)

WS_API_URL = os.getenv("WS_API_URL")
client_id = "chatbot"

pattern = "([A-Z]+)\\*([0-9]+)"


def process(msg: str):
    content = json.loads(msg)
    ma = re.findall(pattern, content["message"])
    if ma:
        print(content["name"], ma)


async def ws_thread():
    async for websocket in websockets.connect(
        f"{WS_API_URL}/chatroom/{client_id}"
    ):
        try:
            async for msg in websocket:
                data = json.loads(msg)
                if data["event-type"] != "chat":
                    continue
                response_data = {
                    "timestamp": int(time.time() * 1000),
                    "event-type": "system",
                    "client-id": client_id,
                    "name": "System",
                    "message": chatbot(msg),
                }
                await websocket.send(json.dumps(response_data))
        except websockets.ConnectionClosed:
            continue


async def run_listener():
    task1 = asyncio.create_task(ws_thread())
    print("chatbot is up")
    await asyncio.gather(task1)


if __name__ == "__main__":
    asyncio.run(run_listener())
