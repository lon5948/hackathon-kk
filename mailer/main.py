import asyncio

import requests
import os
import time
from dotenv import load_dotenv
from mailer.dump import dump_and_email

load_dotenv()

KKSTREAM_BASE_URL = os.getenv("KKSTREAM_BASE_URL", "https://api.one-stage.kkstream.io/bv/cms/v1/lives/")
API_KEY = os.getenv("API_KEY")
ORG_ID = os.getenv("ORG_ID")
STREAM_ID = os.getenv("STREAM_ID")
CHECK_STREAM_SESSION = int(os.getenv("CHECK_STREAM_SESSION", "60"))

url = KKSTREAM_BASE_URL + STREAM_ID

headers = {
    "x-bv-org-id": ORG_ID,
    "Accept": "application/json",
    "authorization": "Bearer " + API_KEY
}


def check_stream_status(url, headers):
    response = requests.get(url, headers=headers)
    data = response.json()

    if data['live']['status'] in ("LIVE_STATUS_CLOSED", "LIVE_STATUS_ENCODING"):
        dump_and_email()
        print('live closed, mail sent')
        return False
    print('live not closed')
    print(data['live']['status'])
    return True


async def run_mailer():
    print("mailer is up")
    while check_stream_status(url, headers):
        time.sleep(CHECK_STREAM_SESSION)


if __name__ == "__main__":
    asyncio.run(run_mailer())
