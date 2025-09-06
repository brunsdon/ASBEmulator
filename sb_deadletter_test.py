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

# Set MaxDeliveryCount low in config for this test (e.g., 3)

def main():
    print("Sending message to test dead-lettering...")
    with ServiceBusClient.from_connection_string(CONN_STR) as client:
        with client.get_topic_sender(topic_name=TOPIC_NAME) as sender:
            msg = ServiceBusMessage("Deadletter test message")
            sender.send_messages(msg)
        print("Message sent.")
        delivery_attempts = 0
        with client.get_subscription_receiver(topic_name=TOPIC_NAME, subscription_name=SUBSCRIPTION_NAME, max_wait_time=5) as receiver:
            for message in receiver:
                print(f"Received: {str(message)} (attempt {delivery_attempts+1})")
                delivery_attempts += 1
                # Do NOT complete the message, so it will be redelivered
                if delivery_attempts >= 4:
                    print("PASS: Message should now be dead-lettered. Check dead-letter queue.")
                    break
        # Try to receive from dead-letter queue
        with client.get_subscription_receiver(topic_name=TOPIC_NAME, subscription_name=SUBSCRIPTION_NAME, sub_queue="deadletter", max_wait_time=5) as dlq_receiver:
            for dlq_message in dlq_receiver:
                print(f"Received from dead-letter queue: {str(dlq_message)}")
                dlq_receiver.complete_message(dlq_message)
                print("PASS: Dead-letter test passed.")
                return

if __name__ == "__main__":
    try:
        main()
    except Exception as ex:
        print(f"FAIL: {ex}")
        sys.exit(3)
