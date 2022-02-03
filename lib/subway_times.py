# from google.transit import gtfs_realtime_pb2
# import requests


from array import array
from nyct_gtfs import NYCTFeed
from datetime import datetime
import math


# Bedford Stop Info
# ID: LO8N (trip.location)
# Index: 18 (trip.current_stop_sequence_index)


class SubwayTimes:
    arrivals = []

    api_key = "qiphNHwN4rHjI4Y0fZQv6dHckEk6S4U6tZ03zEw6"
    train = "L"
    feed = NYCTFeed(train, api_key=api_key)

    def __init__(self, train="L"):
        self.train = train
        self.get_subway_times()

    def get_subway_times(
        self, travel_direction="N", headed_for_stop="L08N", underway=True
    ):
        trips = self.feed.filter_trips(
            travel_direction=travel_direction,
            headed_for_stop_id=headed_for_stop,
            underway=underway,
        )

        # self.feed.refresh()

        self.arrivals = []
        for trip in trips[:2]:
            # print("Last Update:", trip.last_position_update)
            # print("Station:", trip._stops.get_station_name(trip.location))
            # print("Status:", trip.location_status)

            try:
                if len(trip.stop_time_updates) > 0:
                    bedford_arrivals = [
                        update
                        for update in trip.stop_time_updates
                        if update.stop_id == "L08N"
                    ]

                    if len(bedford_arrivals) == 0:
                      continue

                    next = bedford_arrivals[0]
                    now = datetime.now()
                    delta = next.arrival - now
                    minutes_away = delta.total_seconds() / 60

                    self.arrivals.append(math.ceil(minutes_away))
            except Exception as err:
                print("error fetching subway times", err)
                continue

            # print(trip.arrival)
            # print("Departure Time: ", trip.departure_time)
            # print("----")

    def upcoming_arrivals(self):
        self.get_subway_times()
        return self.arrivals


arrivals = SubwayTimes().upcoming_arrivals()
print(arrivals)
