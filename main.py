import asyncio
from listener import run_listener
from mailer import run_mailer


async def create_threads():
    tasks = [asyncio.create_task(run_listener()), asyncio.create_task(run_mailer())]
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(create_threads())
