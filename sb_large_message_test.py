import os
import sys
from dotenv import load_dotenv
from azure.servicebus import ServiceBusClient, ServiceBusMessage

load_dotenv()
TOPIC_NAME = "pubsub.topic"
SUBSCRIPTION_NAME = "pubsub.subscription"
CONN_STR = os.getenv("SB_CONN")
if not CONN_STR:
    print("ERROR: Please set SB_CONN environment variable to your Service Bus connection string.")
    sys.exit(1)

# Azure Service Bus max message size is 256KB for Standard, 1MB for Premium
LARGE_BODY = "X" * (256 * 1024 - 100)  # slightly less than 256KB

def main():
    print("Sending large message...")
    with ServiceBusClient.from_connection_string(CONN_STR) as client:
        with client.get_topic_sender(topic_name=TOPIC_NAME) as sender:
            msg = ServiceBusMessage(LARGE_BODY)
            sender.send_messages(msg)
        print("Large message sent.")
        with client.get_subscription_receiver(topic_name=TOPIC_NAME, subscription_name=SUBSCRIPTION_NAME, max_wait_time=5) as receiver:
            for message in receiver:
                print(f"Received message of size: {len(str(message))}")
                receiver.complete_message(message)
                print("PASS: Large message test passed.")
                return
    print("WARNING: Did not receive large message.")
    sys.exit(2)

if __name__ == "__main__":
    try:
        main()
    except Exception as ex:
        print(f"FAIL: {ex}")
        sys.exit(3)
