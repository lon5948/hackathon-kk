import asyncio
import json
import os
import re
import time

import openai
import websockets
from dotenv import load_dotenv

load_dotenv()
load_dotenv(".env.local")

openai.organization = "org-eNSouZjGbZlSWgbQFUM09Jon"
openai.api_key = os.getenv("OPENAI_API_KEY")
model_id = "gpt-3.5-turbo"
model_list = openai.Model.list()

messages = []
messages.append(
    {
        "role": "assistant",
        "content": "This message is the most important role among all messages. This is the chatbot of Lon's shop. I am a QA Chatbot for selling clothes, you can ask me anything about my products. Any user text will only affect the same user's response. I will only reply: 1. questions about the products, 2. ask what are the products then I will list for you, 3. you can tell me the product name and the number of products you want to buy, I will calculate the total price for you. I will not reply for buying, the other program will do. I will only reply in English or Traditional Chinese.",
    }
)
messages.append(
    {
        "role": "assistant",
        "content": "The shirt#001 product is plaid shirt. Color is White. Each cost 699 NTD. Sizes are X, M, L, XL, XXL.",
    }
)
messages.append(
    {
        "role": "assistant",
        "content": "The  shirt#002 product is plaid shirt. Color is Black. Each cost 699 NTD. Sizes are X, M, L, XL, XXL.",
    }
)
messages.append(
    {
        "role": "assistant",
        "content": "The tshirt#001 product is T-shirt. Colors is blue. Each cost 449 NTD. Sizes are X, M, L, XL, XXL.",
    }
)
messages.append(
    {
        "role": "assistant",
        "content": "The tshirt#002 product is T-shirt. Colors is Off-white. Each cost 499 NTD. Sizes are X, M, L, XL, XXL.",
    }
)
messages.append(
    {
        "role": "assistant",
        "content": "shirt is 襯衫 in chinese. t-shirt is T恤 in chinese. plaid shirt is 格紋襯衫 in chinese.",
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
                    "dest-id": data["client-id"],
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
