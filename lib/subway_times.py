from nyct_gtfs import NYCTFeed
from datetime import datetime
import math
import os


# Bedford Stop Info
# ID: LO8N, LO8S

# Greenpoint Stop
# ID: G28N, G28S


class SubwayTimes:
    api_key = os.getenv("MTA_API_KEY", "qiphNHwN4rHjI4Y0fZQv6dHckEk6S4U6tZ03zEw6")
    feed = None

    # The line-name for a train e.g. "G" or "L"
    train = None

    def __init__(self, train=None):
        self.train = train
        self.feed = NYCTFeed(train, api_key=self.api_key)

    def refresh(self):
        self.feed.refresh()

    def arrivals_for(self, stop_id=None, direction=None):
        trips = self.feed.filter_trips(
            headed_for_stop_id=stop_id, travel_direction=direction, underway=True
        )

        arrivals = []
        for trip in trips:
            try:
                if len(trip.stop_time_updates) > 0:
                    stop_arrivals = [
                        update
                        for update in trip.stop_time_updates
                        if update.stop_id == stop_id
                    ]

                    if len(stop_arrivals) == 0:
                        continue

                    arrivals.append(Arrival(stop_arrivals[0]))
            except Exception as err:
                print(f"error fetching subway times for {stop_id}", err)
                continue

        return arrivals


class Arrival:
    _trip_update = None

    def __init__(self, trip_update) -> None:
        self._trip_update = trip_update

    @property
    def minutes_away(self) -> int:
        return math.ceil(
            (self._trip_update.arrival - datetime.now()).total_seconds() / 60
        )

    def is_makeable(self, walk_time=0) -> bool:
        return self.minutes_away > walk_time


# times = SubwayTimes(train="G")
# g_times = times.feed.filter_trips(line_id="G")
# court_sq = times.arrivals_for(stop_id="G28N", direction="N")
# church_ave = times.arrivals_for(stop_id="G28S", direction="S")
# eighth_ave = times.arrivals_for(stop_id="L08N", direction="N")
# canarsie = times.arrivals_for(stop_id="L08N", direction="S")
