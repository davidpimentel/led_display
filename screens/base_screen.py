class BaseScreen:
    def __init__(self, display_indefinitely=False, duration=30):
        self.display_indefinitely = display_indefinitely
        self.duration = duration

    def fetch_data(self):
        """
        Return any externally fetched data in this method
        """
        pass

    def fetch_data_interval(self):
        """
        interval, in seconds, between fetch_data calls, or None if there is no data to fetch
        """
        return None

    def render(self, canvas, data):
        """
        main rendering method
        """
        raise Exception("render() not implemented")

    def animation_interval(self):
        """
        interval, in seconds, between render() calls when there are no changes to data, or None
        if the screen should only re-render when the data changes
        """
        return None

    def display_duration(self):
        """
        How long, in seconds, the screen should be displayed, or None if the screen should
        be displayed indefinitely
        """
        return None if self.display_indefinitely else self.duration
