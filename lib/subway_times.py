# from google.transit import gtfs_realtime_pb2
# import requests


from nyct_gtfs import NYCTFeed


# Bedford Stop Info
# ID: LO8N (trip.location)
# Index: 18 (trip.current_stop_sequence_index)


class SubwayTimes:
    def __init__(self):
        self.get_subway_times()

    def get_subway_times(self):
        feed = NYCTFeed("L", api_key="qiphNHwN4rHjI4Y0fZQv6dHckEk6S4U6tZ03zEw6")
        trips = feed.filter_trips(
            travel_direction="N", headed_for_stop_id="L08N", underway=True
        )

        feed.refresh()
        for trip in trips:
            print("Last Update:", trip.last_position_update)
            print("Station:", trip._stops.get_station_name(trip.location))
            print("Status:", trip.location_status)
            print(trip.current_stop_sequence_index)
            print(trip.stop_time_updates[0])
            # print(trip.arrival)
            # print("Departure Time: ", trip.departure_time)
            print("----")


SubwayTimes()
