import asyncio
import json
import time
import pandas as pd
import os
import re

import websockets
from dotenv import load_dotenv

load_dotenv()

WS_API_URL = os.getenv("WS_API_URL")
clientId = "listener"

pattern = "([A-Z]+)\\*([0-9]+)"
items_df = pd.DataFrame()
orders_df = pd.DataFrame()


def process(msg: str):
    content = json.loads(msg)
    ma = re.findall(pattern, content["message"])
    if ma:
        print(content["name"], ma)
        update_orders(content, ma)


def update_orders(content: dict, orders: list):
    global orders_df, items_df
    for (item, count) in orders:
        count = int(count)
        if count < 0:
            continue
        item_name = items_df.where(items_df["abr"] == item).dropna()
        if item_name.empty:
            continue
        item_name = item_name.item_name.values[0]
        item_remaining_count = items_df.where(items_df["item_name"] == item_name).dropna().remaining_count.values[0]
        item_remaining_count = int(item_remaining_count)
        print(item_name, count, item_remaining_count)
        # print(item, item_name, type(item_count), item_count, type(ordered_count), ordered_count)
        if count > item_remaining_count:
            continue
        order_content = {
            "name": [content["name"]],
            "address": [content["address"]],
            "email": [content["email"]],
            "item_name": [item_name],
            "count": [count]
        }
        new_orders_df = pd.DataFrame(data=order_content)
        new_df = pd.concat([orders_df, new_orders_df])
        new_df.to_csv("./output/orders.csv", encoding='utf-8', index=False)
        orders_df = new_df.copy()

        items_df.loc[items_df['item_name'] == item_name, 'remaining_count'] = item_remaining_count - count
        items_df.to_csv("./output/items.csv", encoding='utf-8', index=False)
        # items_df = new_items_df.copy()


def get_df():
    global items_df, orders_df
    df = process_csv("./output/items.csv")
    items_df = df.copy()
    df = process_csv("./output/orders.csv")
    orders_df = df.copy()


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


async def update_df_thread():
    while True:
        get_df()
        await asyncio.sleep(1)


async def item_txt_thread():
    global items_df
    with open("./output/item_output.txt", "w") as f:
        while True:
            await asyncio.sleep(1)
            f.seek(0)
            f.truncate()
            t = time.strftime('%c')
            f.write(f"{t}\n{items_df.to_markdown(index=False, tablefmt='simple', numalign='left', stralign='left')}\n")
            f.flush()
            os.fsync(f.fileno())


async def order_txt_thread():
    global orders_df
    with open("./output/order_output.txt", "w") as f:
        while True:
            await asyncio.sleep(1)
            f.seek(0)
            f.truncate()
            f.write(f"""{orders_df[['name', 'item_name', 'count']].tail(5).to_markdown(index=False,
                                                                                     tablefmt='simple', 
                                                                                     numalign='left', 
                                                                                     stralign='left')}\n""")
            f.flush()
            os.fsync(f.fileno())


async def run_listener():
    task1 = asyncio.create_task(ws_thread())
    task2 = asyncio.create_task(update_df_thread())
    task3 = asyncio.create_task(item_txt_thread())
    task4 = asyncio.create_task(order_txt_thread())
    print("listener is up")
    await asyncio.gather(task1, task2, task3, task4)


if __name__ == "__main__":
    asyncio.run(run_listener())
