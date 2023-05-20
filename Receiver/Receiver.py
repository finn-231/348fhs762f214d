import pika
from DataWriter import DataWriter


class Receiver:

    RABBITMQ_HOST = "localhost"
    RABBITMQ_QUEUE = "answer"

    def __init__(self):

        # Start the RabbitMQ consumer
        self.start_rabbitmq_consumer()

    # Function to process the received data
    def process_data(self, data):

        # Print the current DataObject for demonstration purposes
        self.write_object(data)


    # Function to delete the DataObject after one minute and write it to the database before
    def write_object(self, data):
        
        writer = DataWriter.DataWriter()
        writer.write_json_data(data)

    # Function to create a new DataObject for the next minute

    # RabbitMQ message handler
    def rabbitmq_callback(self, ch, method, properties, body):
        # Convert the received data to a string
        data = body.decode("utf-8")
        print(data)
        # Process the received data
        self.process_data(data)

    # Connect to RabbitMQ and start consuming messages
    def start_rabbitmq_consumer(self):
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.RABBITMQ_HOST))
        channel = connection.channel()

        # Declare the queue
        channel.queue_declare(queue=self.RABBITMQ_QUEUE)

        # Set up the callback for incoming messages
        channel.basic_consume(
            queue=self.RABBITMQ_QUEUE, on_message_callback=self.rabbitmq_callback, auto_ack=True
        )

        # Start consuming messages
        print("Waiting for messages...")
        channel.start_consuming()
