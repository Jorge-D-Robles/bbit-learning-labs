import pika
import sys

class mqConsumer:
    def __init__(
        self, binding_key: str, exchange_name: str, queue_name: str
    ) -> None:
        self.binding_key = binding_key
        self.exchange_name = exchange_name
        self.queue_name = queue_name

        self.setupRMQConnection()


    def setupRMQConnection(self) -> None:
        self.connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))

        # Establish Channel
        self.channel = self.connection.channel()

        # Create Queue if not already present
        self.channel.exchange_declare(exchange='logs', exchange_type='fanout')

        # Create the exchange if not already present
        result = self.channel.queue_declare(queue='', exclusive=True)
        queue_name = result.method.queue

        # Bind Binding Key to Queue on the exchange
        self.channel.queue_bind(exchange='logs', queue=queue_name)

        # Set-up Callback function for receiving messages
        def callback(ch, method, properties, body):
            print(f" [x] {body}")


    def on_message_callback(
        self, channel, method_frame, header_frame, body
    ) -> None:
        # Acknowledge message
        channel.basic_ack(method_frame.delivery_tag, False)

        #Print message (The message is contained in the body parameter variable)
        print(body)


    def startConsuming(self) -> None:
        # Print " [*] Waiting for messages. To exit press CTRL+C"
        print(" [*] Waiting for messages. To exit press CTRL+C")
        # Start consuming messages
        self.channel.start_consuming()


    def __del__(self) -> None:
        # Print "Closing RMQ connection on destruction"
        print("Closing RMQ connection on destruction")
        # Close Channel
        self.channel.close()
        # Close Connection
        self.connection.close()
