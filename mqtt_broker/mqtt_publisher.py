import paho.mqtt.client as mqtt
from fake_sensor.weather_sensor import WeatherSensor
import json
from time import sleep


class MqttPublisher:

    def __init__(self, host, port, topic, interval):
        self.broker_host = host
        self.broker_port = port
        self.topic = topic
        self.interval = interval
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.connect(host, port)

    def publish_to_mqtt(self, data):
        print(data)
        payload = json.dumps(data)
        ret = self.mqtt_client.publish(self.topic, payload)
        if ret[0] != mqtt.MQTT_ERR_SUCCESS:
            print("Error publishing data")
        else:
            print("data published successfully")


if __name__ == '__main__':
    broker_host = '127.0.0.1'
    broker_port = 1883
    broker_topic = 'weather'
    publish_interval = 5
    w_sensor = WeatherSensor(csv_filepath='../data/homeA2014.csv')
    publisher = MqttPublisher(broker_host, broker_port, broker_topic, publish_interval)
    reader = w_sensor.get_data_from_dataset()
    while True:
        sensor_data = next(reader)
        publisher.publish_to_mqtt(sensor_data)
        sleep(publisher.interval)
