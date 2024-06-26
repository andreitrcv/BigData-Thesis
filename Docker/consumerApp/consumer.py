from confluent_kafka import Consumer, KafkaException
import sys
import os
import time

# Kafka broker host and port
# bootstrap_servers = 'localhost:9092'
kafka_broker = os.getenv('KAFKA_BOOTSTRAP_SERVERS')

# Kafka topic to consume from
topic = 'telemetry'
# Consumer group id
group_id = 'test_consumer_group'

# Output file path
output_file = 'telemetry_messages.txt'

# Kafka consumer configuration
conf = {
    'bootstrap.servers': kafka_broker,
    'group.id': group_id,
    'auto.offset.reset': 'earliest'  # Read from the beginning of the topic
}

def kafka_consumer():
    # Create Kafka Consumer instance
    consumer = Consumer(conf)

    try:
        # Subscribe to topic
        consumer.subscribe([topic])

        with open(output_file, 'a') as file:
            while True:
                # Poll for messages
                msg = consumer.poll(timeout=1.0)  # Timeout in seconds

                if msg is None:
                    continue
                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        continue
                    else:
                        print(msg.error())
                        break

                # Write message to file
                file.write(msg.value().decode('utf-8') + '\n')

    except KeyboardInterrupt:
        sys.stderr.write('Aborted by user\n')

    finally:
        # Close Kafka Consumer
        consumer.close()

if __name__ == '__main__':
    time.sleep(30)
    kafka_consumer()

