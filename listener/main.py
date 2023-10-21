import asyncio
import json
import time
import pandas as pd
import numpy as np
import os
import re

import websockets
from dotenv import load_dotenv

load_dotenv()

WS_API_URL = os.getenv("WS_API_URL")
clientId = "listener"

pattern = "([A-Z]+)\\*([0-9]+)"
items_df = None


def process(msg: str):
    content = json.loads(msg)
    ma = re.findall(pattern, content["message"])
    if ma:
        print(content["name"], ma)
        update_orders(content, ma)


def update_orders(content: dict, orders: list):
    orders_df = process_csv("../output/orders.csv")
    for (item, count) in orders:
        count = int(count)
        if count < 0:
            continue
        item_name = items_df.where(items_df["abr"] == item)
        if item_name.empty:
            continue
        item_name = item_name.item_name.values[0]
        item_count = items_df.where(items_df["item_name"] == item_name).total_count.values[0]
        ordered_count = orders_df.where(orders_df["item_name"] == item_name)["count"].sum()
        print(item, item_name, type(item_count), item_count, type(ordered_count), ordered_count)
        if ordered_count + count > item_count:
            continue
        order_content = {
            "name": [content["name"]],
            "address": [content["address"]],
            "email": [content["email"]],
            "item_name": [item_name],
            "count": [count]
        }
        new_order_df = pd.DataFrame(data=order_content)
        new_df = pd.concat([orders_df, new_order_df])
        new_df.to_csv("../output/orders.csv", encoding='utf-8', index=False)


def get_items():
    df = process_csv("../output/items.csv")
    global items_df
    items_df = df.copy()


def process_csv(filename: str) -> pd.DataFrame:
    data = pd.read_csv(filename)
    return data


async def ws_thread():
    async for websocket in websockets.connect(
        f"{WS_API_URL}/chatroom/{clientId}"
    ):
        try:
            async for msg in websocket:
                process(msg)
        except websockets.ConnectionClosed:
            continue


async def item_thread():
    while True:
        get_items()
        await asyncio.sleep(1)


async def txt_thread():
    with open("../output/output.txt", "w") as f:
        while True:
            await asyncio.sleep(1)
            f.seek(0)
            f.truncate()
            t = time.strftime('%c')
            f.write(f"{t}\n{items_df.to_string(index=False, justify='center')}\n")
            f.flush()
            os.fsync(f.fileno())


async def main():
    task1 = asyncio.create_task(ws_thread())
    task2 = asyncio.create_task(item_thread())
    task3 = asyncio.create_task(txt_thread())
    await asyncio.gather(task1, task2, task3)


if __name__ == "__main__":
    asyncio.run(main())
