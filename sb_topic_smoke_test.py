import os
import sys
import uuid
import time
from dotenv import load_dotenv
from azure.servicebus import ServiceBusClient, ServiceBusMessage

load_dotenv()

# Topic and subscription names (update as needed)
TOPIC_NAME = "topic.1"
SUBSCRIPTION_NAME = "subscription.1"

# Read connection string from env var
CONN_STR = os.getenv("SB_CONN")
if not CONN_STR:
    print("ERROR: Please set SB_CONN environment variable to your Service Bus connection string.")
    sys.exit(1)

def main():
    # Unique payload to verify round-trip
    run_id = str(uuid.uuid4())
    body = f"hello from python topic smoke test | run_id={run_id}"

    print(f"Using connection string: {CONN_STR}")
    print(f"Target topic: {TOPIC_NAME}")
    print(f"Target subscription: {SUBSCRIPTION_NAME}")
    print("Opening client...")

    # Create a ServiceBusClient and send/receive a message
    with ServiceBusClient.from_connection_string(CONN_STR) as client:
        # 1) SEND
        print("Sending a test message to topic...")
        with client.get_topic_sender(topic_name=TOPIC_NAME) as sender:
            msg = ServiceBusMessage(body)
            sender.send_messages(msg)
        print("Message sent.")

        # Small delay to allow broker to commit
        time.sleep(0.5)

        # 2) RECEIVE
        print("Receiving message from subscription...")
        with client.get_subscription_receiver(
            topic_name=TOPIC_NAME,
            subscription_name=SUBSCRIPTION_NAME,
            max_wait_time=5
        ) as receiver:
            for message in receiver:
                text = str(message)
                print(f"Received: {text}")
                # verify it’s the one we just sent
                if run_id in text:
                    receiver.complete_message(message)
                    print("PASS: End-to-end OK (matched run_id and completed message).")
                    return
                else:
                    # Not our message (subscription had older messages) — settle and keep looking
                    receiver.complete_message(message)
                    print("Info: received a different message; continuing to look...")

    print("WARNING: Did not receive our test message within the wait window.")
    sys.exit(2)

if __name__ == "__main__":
    try:
        main()
    except Exception as ex:
        print(f"FAIL: {ex}")
        sys.exit(3)
