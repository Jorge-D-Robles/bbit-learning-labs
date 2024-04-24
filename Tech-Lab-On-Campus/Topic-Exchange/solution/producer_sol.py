import producer_interface as p
import pika # type: ignore
import os
import sys
class mqProducer(p.mqProducerInterface):
    def __init__(self, routing_key: str, exchange_name: str) -> None:
        # Save parameters to class variables
        self.routing_key = routing_key
        self.exchange_name = exchange_name
        #setting ticker/price/sector from arguments in command line

        self.setupRMQConnection()
        # Call setupRMQConnection

    def setupRMQConnection(self) -> None:
        # Set-up Connection to RabbitMQ service
        con_params = pika.URLParameters(os.environ["AMQP_URL"])
        self.connection = pika.BlockingConnection(parameters=con_params)
        # Establish Channel
        self.channel = self.connection.channel()
        # Create the exchange if not already present
        self.channel.exchange_declare(exchange=self.exchange_name, exchange_type="topic")

    def publishOrder(self, message: str) -> None:
        # Basic Publish to Exchange
        message = message.encode("utf-8")

        self.channel.basic_publish(exchange=self.exchange_name, routing_key=self.routing_key, body=message)
        print(f" [x] Sent {self.routing_key}:{message}")
        print(f"Closing RMQ connection on destruction")
        # Close Channel
        self.channel.close()
        # Close Connection
        self.connection.close()

        # Create Appropiate Topic String

        # Send serialized message or String

        # Print Confirmation

        # Close channel and connection
# We'll first set up the connection and channel
# connection = pika.BlockingConnection(
#     pika.ConnectionParameters(host='localhost'))
# channel = connection.channel()

# # Declare the topic exchange
# channel.exchange_declare(exchange='topic_logs', exchange_type='topic')

# # Set the routing key and publish a message with that topic exchange:
# routing_key = sys.argv[1] if len(sys.argv) > 2 else 'anonymous.info'
# message = ' '.join(sys.argv[2:]) or 'Hello World!'
# channel.basic_publish(
#     exchange='topic_logs', routing_key=routing_key, body=message)
# print(f" [x] Sent {routing_key}:{message}")
