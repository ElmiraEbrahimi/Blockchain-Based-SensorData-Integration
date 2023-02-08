import paho.mqtt.client as mqtt
import json
from time import sleep
from fake_sensor.weather_sensor import WeatherSensor
from utils.database_commands import get_interval_publish_to_broker_from_sqlite


class MqttPublisher:

    def __init__(self, address, port, topic, interval):
        self.broker_address = address
        self.broker_port = port
        self.topic = topic
        self.interval = interval
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.connect(address, port)

    def publish_to_mqtt(self, data):
        print(data)
        payload = json.dumps(data)
        mid = self.mqtt_client.publish(self.topic, payload)
        if mid[0] != mqtt.MQTT_ERR_SUCCESS:
            print("Error publishing data")
        else:
            print("data published successfully")


if __name__ == '__main__':
    broker_address = '127.0.0.1'
    broker_port = 1883
    broker_topic = 'weather'
    sqlite_filepath = '../django_website/db.sqlite3'
    publish_interval = get_interval_publish_to_broker_from_sqlite(sqlite_filepath)


    w_sensor = WeatherSensor(dataset_csv_filepath='../data/homeA2014.csv')
    publisher = MqttPublisher(broker_address, broker_port, broker_topic, publish_interval)
    reader = w_sensor.get_data_from_dataset()
    while True:
        sensor_data = next(reader)
        publisher.publish_to_mqtt(sensor_data)
        publisher.interval = get_interval_publish_to_broker_from_sqlite(sqlite_filepath)
        sleep(publisher.interval)
