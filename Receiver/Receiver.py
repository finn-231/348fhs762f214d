

import pika
import threading
import DataObject
import time

# RabbitMQ connection parameters
RABBITMQ_HOST = 'localhost'
RABBITMQ_QUEUE = 'answer'
RABBITMQ_REQUEST_QUEUE = 'request'
INTERVAL = 60

# Function to process the received data
def process_data(data, data_object):
    # Add the received data to the current DataObject
    data_object.add_data(data)
    
    # Print the current DataObject for demonstration purposes
    print(f"Received data: {data}")
    # print(f"Current DataObject data: {data_object.data}")
    # print(f"Current DataObject timestamp: {data_object.timestamp}")

def send_request():
    
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    channel = connection.channel()
    
    # Declare the queue
    channel.queue_declare(queue=RABBITMQ_REQUEST_QUEUE)
    
    while True:
        # Send "hello" message to the queue every 60 seconds
        channel.basic_publish(exchange='', routing_key=RABBITMQ_REQUEST_QUEUE, body="x")
        print("Request sent to all units on channel 'request'")
        time.sleep(INTERVAL)  # Wait for 60 seconds before sending the next request

    # Close the connection
    connection.close()

# Function to delete the DataObject after one minute
def delete_object(data_object):
    print(f"Deleting DataObject with timestamp {data_object.timestamp} \nIt included the following data: {data_object.data}")
    del data_object

    # Create a new DataObject for the next minute
    create_new_object()

# Function to create a new DataObject for the next minute
def create_new_object():
    data_object = DataObject.DataObject()

    # Schedule the deletion of the DataObject after one minute
    threading.Timer(INTERVAL, delete_object, args=[data_object]).start()

# RabbitMQ message handler
def rabbitmq_callback(ch, method, properties, body):
    # Convert the received data to a string
    data = body.decode('utf-8')
    
    # Process the received data
    process_data(data, current_data_object)

# Connect to RabbitMQ and start consuming messages
def start_rabbitmq_consumer():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    channel = connection.channel()
    
    # Declare the queue
    channel.queue_declare(queue=RABBITMQ_QUEUE)
    
    # Set up the callback for incoming messages
    channel.basic_consume(queue=RABBITMQ_QUEUE, on_message_callback=rabbitmq_callback, auto_ack=True)
    
    # Start consuming messages
    print("Waiting for messages...")
    channel.start_consuming()

# start method of the receiver
def initial_start():
    global current_data_object
    current_data_object = DataObject.DataObject()

    # Schedule the deletion of the initial DataObject after one minute
    threading.Timer(INTERVAL, delete_object, args=[current_data_object]).start()



    # notify_thread = threading.Thread(target=send_request)
    # notify_thread.daemon = True  # Set the thread as a daemon thread
    # notify_thread.start()

    # Start the RabbitMQ consumer
    start_rabbitmq_consumer()




# only demo
initial_start()