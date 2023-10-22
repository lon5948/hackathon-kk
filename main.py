import asyncio
from listener import run_listener
from mailer import run_mailer
import multiprocessing


def run_async_function(func):
    asyncio.run(func())


if __name__ == "__main__":
    process1 = multiprocessing.Process(target=run_async_function, args=(run_listener,))
    process2 = multiprocessing.Process(target=run_async_function, args=(run_mailer,))

    # Start the processes
    process1.start()
    process2.start()

    # Join the processes (this will block the main program until the child processes finish)
    process1.join()
    process2.join()
