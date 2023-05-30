import pika
from Modules.DataWriter.DataWriter import DataWriter
from Modules.DataReader.DataReader import DataReader


class Receiver:
    from Credentials import storecreds as cfg

    RABBITMQ_HOST = cfg.rabbitmq["host"]
    RABBITMQ_QUEUE = cfg.rabbitmq["queue"]

    def __init__(self):
        pass

    def getdatawithquery(self, query):
        dr = DataReader()
        dr.connect()
        result = dr.custom_query(query)
        return result
    
    def getdataonefield(self, table, field):
        dr = DataReader()
        dr.connect()
        result = dr.get_single_field(table_name=table, field=field)
        return result
    
    # Function to process the received data
    def process_data(self, data):
        parseddata = self.write_object(data)
        return parseddata

    # Function to delete the DataObject after one minute and write it to the database before
    def write_object(self, data):
        writer = DataWriter()
        parseddata = writer.write_json_data(data)
        return parseddata

    # Function to create a new DataObject for the next minute

    # RabbitMQ message handler
    def rabbitmq_callback(self, ch, method, properties, body):
        # Convert the received data to a string
        data = body.decode("utf-8")
        # Process the received data
        parseddata = self.process_data(data)
        id = parseddata.get('unit_id')
        print(f"#[Receiver]: Message received from Unit with ID {id}.\n")

    # Connect to RabbitMQ and start consuming messages
    def start_rabbitmq_consumer(self):
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=self.RABBITMQ_HOST)
        )
        channel = connection.channel()

        # Declare the queue
        channel.queue_declare(queue=self.RABBITMQ_QUEUE)

        # Set up the callback for incoming messages
        channel.basic_consume(
            queue=self.RABBITMQ_QUEUE,
            on_message_callback=self.rabbitmq_callback,
            auto_ack=True,
        )

        # Start consuming messages
        print(
            f"#[Receiver]: Started listening on queue {self.RABBITMQ_QUEUE}. Waiting for messages...\n"
        )
        channel.start_consuming()
