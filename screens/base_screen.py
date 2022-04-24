class BaseScreen:
    def fetch_data(self):
        pass

    def fetch_data_delay(self):
        return None

    def render(self, data):
        raise Exception("render() not implemented")

    def animation_delay(self):
        return None
