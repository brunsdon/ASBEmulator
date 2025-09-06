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

BATCH_SIZE = 5

def main():
    print("Sending batch of messages...")
    with ServiceBusClient.from_connection_string(CONN_STR) as client:
        with client.get_topic_sender(topic_name=TOPIC_NAME) as sender:
            messages = [ServiceBusMessage(f"Batch message {i}") for i in range(BATCH_SIZE)]
            sender.send_messages(messages)
        print("Batch sent.")
        received = 0
        with client.get_subscription_receiver(topic_name=TOPIC_NAME, subscription_name=SUBSCRIPTION_NAME, max_wait_time=5) as receiver:
            for message in receiver:
                print(f"Received: {str(message)}")
                receiver.complete_message(message)
                received += 1
                if received == BATCH_SIZE:
                    print("PASS: Batch test passed.")
                    return
    print("WARNING: Did not receive all batch messages.")
    sys.exit(2)

if __name__ == "__main__":
    try:
        main()
    except Exception as ex:
        print(f"FAIL: {ex}")
        sys.exit(3)
