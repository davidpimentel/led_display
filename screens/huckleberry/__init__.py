import asyncio
import os
import sys
import time
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta, timezone

import aiohttp
from huckleberry_api import HuckleberryAPI

from lib.colors import Colors
from lib.ui import Positioned, Stack, Text
from screens.base_screen import BaseScreen


@dataclass
class HuckleberryState:
    bottle_ago: str = ""
    diaper_ago: str = ""


def _format_ago(seconds: float) -> str:
    if seconds < 0:
        return "0m"
    minutes = int(seconds / 60)
    if minutes < 60:
        return f"{minutes}m"
    hours = int(minutes / 60)
    mins = minutes % 60
    if hours < 24:
        return f"{hours}h {mins}m" if mins else f"{hours}h"
    days = int(hours / 24)
    hrs = hours % 24
    return f"{days}d {hrs}h" if hrs else f"{days}d"


class Screen(BaseScreen[HuckleberryState]):
    def __init__(self):
        super().__init__(initial_state=HuckleberryState())
        self.email = os.getenv("HUCKLEBERRY_EMAIL", "")
        self.password = os.getenv("HUCKLEBERRY_PASSWORD", "")
        self.child_uid = os.getenv("HUCKLEBERRY_CHILD_UID", "")
        self.timezone = os.getenv("HUCKLEBERRY_TIMEZONE", "America/New_York")

    def setup(self):
        self.run_on_interval(self._fetch_data, seconds=60)

    def _fetch_data(self):
        async def _async_fetch():

            connector = aiohttp.TCPConnector(force_close=True)
            async with aiohttp.ClientSession(connector=connector) as session:
                api = HuckleberryAPI(
                    email=self.email,
                    password=self.password,
                    timezone=self.timezone,
                    websession=session,
                )
                await api.authenticate()

                now = datetime.now(tz=UTC)
                seven_days_ago = now - timedelta(days=7)

                feed_intervals = await api.list_feed_intervals(
                    self.child_uid, seven_days_ago.timestamp(), now.timestamp()
                )

                bottle_intervals = [
                    i
                    for i in feed_intervals
                    if hasattr(i, "mode") and i.mode == "bottle"
                ]

                diaper_intervals = await api.list_diaper_intervals(
                    self.child_uid, seven_days_ago.timestamp(), now.timestamp()
                )

                now_ts = time.time()
                bottle_ago = ""
                if bottle_intervals:
                    latest = max(bottle_intervals, key=lambda i: float(i.start))
                    bottle_ago = _format_ago(now_ts - float(latest.start))

                diaper_ago = ""
                if diaper_intervals:
                    latest = max(diaper_intervals, key=lambda i: float(i.start))
                    diaper_ago = _format_ago(now_ts - float(latest.start))

                return bottle_ago, diaper_ago

        bottle_ago, diaper_ago = asyncio.run(_async_fetch())
        self.set_state(bottle_ago=bottle_ago, diaper_ago=diaper_ago)

    def build(self, state: HuckleberryState):
        if not state.bottle_ago:
            return Stack(
                children=[
                    Positioned(
                        x=24, y=10, child=Text("...", font="5x8", color=Colors.white)
                    )
                ]
            )

        bottle_label = Text("BTL:", font="5x8", color=Colors.white)
        diaper_label = Text("DPR:", font="5x8", color=Colors.white)
        offset = 4
        return Stack(
            children=[
                Positioned(x=offset, y=4, child=bottle_label),
                Positioned(
                    x=offset + bottle_label.width,
                    y=4,
                    child=Text(state.bottle_ago, font="5x8", color=Colors.teal),
                ),
                Positioned(x=offset, y=18, child=diaper_label),
                Positioned(
                    x=offset + diaper_label.width,
                    y=18,
                    child=Text(state.diaper_ago, font="5x8", color=Colors.green),
                ),
            ]
        )
