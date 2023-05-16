import pika

# RabbitMQ connection parameters
RABBITMQ_HOST = 'localhost'
RABBITMQ_QUEUE = 'answer'
RABBITMQ_REQUEST_QUEUE = 'request'

# RabbitMQ message handler
def rabbitmq_callback(ch, method, properties, body):
    # Convert the received data to a string
    data = body.decode('utf-8')
    
    # Process the received data
    print(f"Received data: {data}")
    
    # Prepare the reply message
    reply_message = f"I am okay"
    
    # Publish the reply message to the reply queue
    publish_reply(reply_message)
    
    # Acknowledge that the message has been processed
    ch.basic_ack(delivery_tag=method.delivery_tag)

# Function to publish the reply message to RabbitMQ
def publish_reply(reply_message):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    channel = connection.channel()
    
    # Declare the reply queue
    channel.queue_declare(queue=RABBITMQ_QUEUE)
    
    # Publish the reply message to the reply queue
    channel.basic_publish(exchange='', routing_key=RABBITMQ_QUEUE, body=reply_message)
    
    # Close the connection
    connection.close()

# Connect to RabbitMQ and start consuming messages
def start_rabbitmq_consumer():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    channel = connection.channel()
    
    # Declare the queue
    channel.queue_declare(queue=RABBITMQ_REQUEST_QUEUE)
    
    # Set up the callback for incoming messages
    channel.basic_consume(queue=RABBITMQ_REQUEST_QUEUE, on_message_callback=rabbitmq_callback)
    
    # Start consuming messages
    print("Waiting for messages...")
    channel.start_consuming()

# Start the RabbitMQ consumer
start_rabbitmq_consumer()
