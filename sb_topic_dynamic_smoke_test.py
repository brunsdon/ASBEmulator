import os
import sys
import uuid
import time
from dotenv import load_dotenv
from azure.servicebus import ServiceBusClient, ServiceBusMessage
from azure.servicebus.management import ServiceBusAdministrationClient

load_dotenv()

TOPIC_NAME = "smoketest.topic"
SUBSCRIPTION_NAME = "smoketest.subscription"

CONN_STR = os.getenv("SB_CONN")
if not CONN_STR:
    print("ERROR: Please set SB_CONN environment variable to your Service Bus connection string.")
    sys.exit(1)

def ensure_topic_and_subscription():
    admin_client = ServiceBusAdministrationClient.from_connection_string(CONN_STR)
    # Create topic if it doesn't exist
    if not admin_client.get_topic_runtime_properties(TOPIC_NAME):
        print(f"Creating topic: {TOPIC_NAME}")
        admin_client.create_topic(TOPIC_NAME)
    else:
        print(f"Topic {TOPIC_NAME} already exists.")
    # Create subscription if it doesn't exist
    if not admin_client.get_subscription_runtime_properties(TOPIC_NAME, SUBSCRIPTION_NAME):
        print(f"Creating subscription: {SUBSCRIPTION_NAME}")
        admin_client.create_subscription(TOPIC_NAME, SUBSCRIPTION_NAME)
    else:
        print(f"Subscription {SUBSCRIPTION_NAME} already exists.")

def main():
    ensure_topic_and_subscription()
    run_id = str(uuid.uuid4())
    body = f"hello from python dynamic topic smoke test | run_id={run_id}"

    print(f"Using connection string: {CONN_STR}")
    print(f"Target topic: {TOPIC_NAME}")
    print(f"Target subscription: {SUBSCRIPTION_NAME}")
    print("Opening client...")

    with ServiceBusClient.from_connection_string(CONN_STR) as client:
        print("Sending a test message to topic...")
        with client.get_topic_sender(topic_name=TOPIC_NAME) as sender:
            msg = ServiceBusMessage(body)
            sender.send_messages(msg)
        print("Message sent.")

        time.sleep(0.5)

        print("Receiving message from subscription...")
        with client.get_subscription_receiver(
            topic_name=TOPIC_NAME,
            subscription_name=SUBSCRIPTION_NAME,
            max_wait_time=5
        ) as receiver:
            for message in receiver:
                text = str(message)
                print(f"Received: {text}")
                if run_id in text:
                    receiver.complete_message(message)
                    print("✅ End-to-end OK (matched run_id and completed message).")
                    return
                else:
                    receiver.complete_message(message)
                    print("Info: received a different message; continuing to look...")
        print("⚠️ Did not receive our test message within the wait window.")
        sys.exit(2)

if __name__ == "__main__":
    try:
        main()
    except Exception as ex:
        print(f"❌ Failure: {ex}")
        sys.exit(3)
