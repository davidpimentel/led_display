import os
from threading import Event, Thread
from uuid import uuid4

from awscrt import mqtt
from awsiot import mqtt_connection_builder


class PubSubClient(Thread):
    def __init__(self, on_message_received=None):
        super().__init__()
        self.on_message_received = on_message_received
        self.stop = Event()
        self.build_mqtt_connection()

    @classmethod
    def is_enabled(cls):
        return (
            os.getenv("AWS_IOT_DEVICE_ENDPOINT") and
            os.getenv("AWS_IOT_DEVICE_CERT_FILENAME") and
            os.getenv("AWS_IOT_DEVICE_PRIVATE_KEY_FILENAME")
        )

    def run(self):
        connect_future = self.mqtt_connection.connect()

        # Future.result() waits until a result is available
        connect_future.result()
        print("connected!")

        subscribe_future, packet_id = self.mqtt_connection.subscribe(
            topic="screen/change_screen",
            qos=mqtt.QoS.AT_LEAST_ONCE,
            callback=self.on_message_received)

        subscribe_result = subscribe_future.result()
        print("subscribed!")

        self.stop.wait()

        # Disconnect
        print("Disconnecting...")
        disconnect_future = self.mqtt_connection.disconnect()
        disconnect_future.result()
        print("Disconnected!")


    def build_mqtt_connection(self):
        current_directory = os.path.dirname(os.path.realpath(__file__))
        self.mqtt_connection = mqtt_connection_builder.mtls_from_path(
            endpoint=os.getenv("AWS_IOT_DEVICE_ENDPOINT"),
            cert_filepath=current_directory + "/.certs/" + os.getenv("AWS_IOT_DEVICE_CERT_FILENAME"),
            pri_key_filepath= current_directory + "/.certs/" + os.getenv("AWS_IOT_DEVICE_PRIVATE_KEY_FILENAME"),
            ca_filepath=current_directory + "/.certs/AmazonRootCA1.cer",
            on_connection_interrupted=self.on_connection_interrupted,
            on_connection_resumed=self.on_connection_resumed,
            client_id="test-" + str(uuid4()),
            clean_session=False,
            keep_alive_secs=30,
            http_proxy_options=None)

    def on_connection_interrupted(self):
        print("on_connection_interrupted")

    def on_connection_resumed(self):
        print("on_connection_resumed")
