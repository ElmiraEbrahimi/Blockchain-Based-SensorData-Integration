import paho.mqtt.client as mqtt
import multiprocessing
import time
from utils.database_commands import get_interval_publish_to_blockchain_from_sqlite
from blockchain.add_sensor_data import add_sensor_data_to_blockchain


class MqttSubscriber:
    def __init__(self, address, port, topic):
        self.broker_address = address
        self.broker_port = port
        self.topic = topic
        self.mqtt_client = mqtt.Client()

    def subscribe_to_mqtt(self, blockchain_queue):
        def on_message(client, userdata, msg):
            received_data = msg.payload.decode()
            blockchain_queue.put(received_data)
            print("[Subscriber] Received data and sent to blockchain queue. Data:", received_data)

        self.mqtt_client.connect(self.broker_address, self.broker_port)
        self.mqtt_client.on_message = on_message
        self.mqtt_client.subscribe(self.topic)
        print('Starting subscriber...')
        self.mqtt_client.loop_forever()


def start_subscriber(blockchain_queue, address, port, topic):
    subscriber = MqttSubscriber(address, port, topic)
    subscriber.subscribe_to_mqtt(blockchain_queue)


def start_sending_to_blockchain(blockchain_queue):
    sqlite_filepath = '../django_website/db.sqlite3'
    while True:
        data = blockchain_queue.get()
        if data is None:
            break
        print(f"[Blockchain Middleware] Received data from queue. Data: {data}")
        print('[Blockchain Middleware] Sending to blockchain...')
        res = add_sensor_data_to_blockchain(data)
        blockchain_publish_interval = get_interval_publish_to_blockchain_from_sqlite(sqlite_filepath)
        time.sleep(blockchain_publish_interval)


#
if __name__ == '__main__':
    broker_address = '127.0.0.1'
    broker_port = 1883
    broker_topic = 'weather'
    queue = multiprocessing.Queue()
    p1 = multiprocessing.Process(target=start_subscriber, args=(queue, broker_address, broker_port, broker_topic))
    p2 = multiprocessing.Process(target=start_sending_to_blockchain, args=(queue,))
    p1.start()
    p2.start()
    while True:
        if not p1.is_alive():
            queue.put(None)
            p2.join()
            break
