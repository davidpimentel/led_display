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

    def __init__(self):
        self.get_subway_times()

    def get_subway_times(
        self, train="L", travel_direction="N", headed_for_stop="L08N", underway=True
    ):
        feed = NYCTFeed(train, api_key=self.api_key)
        trips = feed.filter_trips(
            travel_direction=travel_direction,
            headed_for_stop_id=headed_for_stop,
            underway=underway,
        )

        feed.refresh()
        for trip in trips:
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

                    update = bedford_arrivals[0]
                    now = datetime.now()
                    delta = update.arrival - now
                    minutes_away = delta.total_seconds() / 60

                    self.arrivals.append(math.ceil(minutes_away))
            except AttributeError:
                # print("no arrival times")
                continue

            # print(trip.arrival)
            # print("Departure Time: ", trip.departure_time)
            # print("----")

    def upcoming_arrivals(self):
        self.get_subway_times()

        if len(self.arrivals) > 0:
            return self.arrivals[0:2]


arrivals = SubwayTimes().upcoming_arrivals()
print(arrivals)
