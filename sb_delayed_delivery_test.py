import os
import sys
import time
from datetime import datetime, timedelta
from dotenv import load_dotenv
from azure.servicebus import ServiceBusClient, ServiceBusMessage

load_dotenv()
TOPIC_NAME = "pubsub.topic"
SUBSCRIPTION_NAME = "pubsub.subscription"
CONN_STR = os.getenv("SB_CONN")
if not CONN_STR:
    print("ERROR: Please set SB_CONN environment variable to your Service Bus connection string.")
    sys.exit(1)


def main():
    print("Sending message with delayed delivery...")
    with ServiceBusClient.from_connection_string(CONN_STR) as client:
        with client.get_topic_sender(topic_name=TOPIC_NAME) as sender:
            scheduled_time = datetime.utcnow() + timedelta(seconds=10)
            msg = ServiceBusMessage("Delayed delivery test message")
            sender.schedule_messages(msg, scheduled_time)
        print(f"Message scheduled for delivery at {scheduled_time} UTC.")
        print("Waiting to receive...")
        time.sleep(12)
        with client.get_subscription_receiver(topic_name=TOPIC_NAME, subscription_name=SUBSCRIPTION_NAME, max_wait_time=5) as receiver:
            for message in receiver:
                print(f"Received: {str(message)}")
                receiver.complete_message(message)
                print("✅ Delayed delivery test passed.")
                return
        print("⚠️ Did not receive delayed message.")
        sys.exit(2)

if __name__ == "__main__":
    try:
        main()
    except Exception as ex:
        print(f"❌ Failure: {ex}")
        sys.exit(3)
