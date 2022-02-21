import os

from Adafruit_IO import MQTTClient


class AdafruitMQTTClient:
  def __init__(self, on_change_screen=None):
    self.on_change_screen = on_change_screen
    self.adafruit_io_username = os.getenv("ADAFRUIT_IO_USERNAME")
    self.adafruit_io_key = os.getenv("ADAFRUIT_IO_KEY")
    self.feed_ids = ["led-display.change-screen"]
    self.client = MQTTClient(self.adafruit_io_username, self.adafruit_io_key)
    self.client.on_connect = self.connected
    self.client.on_disconnect = self.disconnected
    self.client.on_message = self.message

  def start(self):
    self.client.connect()
    self.client.loop_background()

  # Define callback functions which will be called when certain events happen.
  def connected(self, client):
    # Connected function will be called when the client is connected to Adafruit IO.
    # This is a good place to subscribe to feed changes.  The client parameter
    # passed to this function is the Adafruit IO MQTT client so you can make
    # calls against it easily.
    print('Connected to Adafruit IO!  Listening for changes...')
    # Subscribe to changes on a feed named DemoFeed.
    for feed_id in self.feed_ids:
      self.client.subscribe(feed_id, qos=1)

  def disconnected(self, client):
    # Disconnected function will be called when the client disconnects.
    print('Disconnected from Adafruit IO!')

  def message(self, client, feed_id, payload):
    # Message function will be called when a subscribed feed has a new value.
    # The feed_id parameter identifies the feed, and the payload parameter has
    # the new value.
    if feed_id == 'led-display.change-screen':
      self.on_change_screen(payload)

