import asyncio
import time
from datetime import UTC, datetime, timedelta

import aiohttp
from huckleberry_api import HuckleberryAPI


async def main() -> None:
    async with aiohttp.ClientSession() as websession:
        api = HuckleberryAPI(
            email="nicolepimentel001@gmail.com",
            password="mRpgCr2u9x$0",
            timezone="Europe/London",
            websession=websession,
        )

        await api.authenticate()

        user_doc = await api.get_user()
        child_uid = user_doc.childList[0].cid

        # print(child_uid)
        now = datetime.now(tz=UTC)
        seven_days_ago = now - timedelta(days=7)
        feed_intervals = await api.list_feed_intervals(
            child_uid, seven_days_ago.timestamp(), now.timestamp()
        )
        # print(feed_intervals)
        bottle_intervals = [
            i for i in feed_intervals if hasattr(i, "mode") and i.mode == "bottle"
        ]

        # print(bottle_intervals)

        diaper_intervals = await api.list_diaper_intervals(
            child_uid, seven_days_ago.timestamp(), now.timestamp()
        )
        # print(diaper_intervals, flush=True)

        now_ts = time.time()
        bottle_ago = ""
        if bottle_intervals:
            latest = max(bottle_intervals, key=lambda i: float(i.start))
            print(latest)
            # bottle_ago = _format_ago(now_ts - float(latest.start))

        diaper_ago = ""
        if diaper_intervals:
            latest = max(diaper_intervals, key=lambda i: float(i.start))
            print(latest)
            # diaper_ago = _format_ago(now_ts - float(latest.start))

        # return bottle_ago, diaper_ago


asyncio.run(main())
