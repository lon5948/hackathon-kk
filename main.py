import asyncio
from listener import run_listener
from mailer import run_mailer
from backend import run_backend
import multiprocessing


async def create_threads(function):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(function())


def run_async_function(func):
    asyncio.run(func())


if __name__ == "__main__":
    process1 = multiprocessing.Process(target=run_async_function, args=(run_listener,))
    # process2 = multiprocessing.Process(target=run_async_function, args=(run_mailer,))
    process3 = multiprocessing.Process(target=run_async_function, args=(run_backend,))

    # Start the processes
    process1.start()
    # process2.start()
    process3.start()

    # Join the processes (this will block the main program until the child processes finish)
    process1.join()
    # process2.join()
    process3.join()




