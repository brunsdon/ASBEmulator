import os
import sys
import uuid
import time
from dotenv import load_dotenv
from azure.servicebus import ServiceBusClient, ServiceBusMessage

load_dotenv()

TOPIC_NAME = "pubsub.topic"
SUBSCRIPTION_NAME = "pubsub.subscription"
MESSAGE_TYPES = ["TypeA", "TypeB", "TypeC"]

CONN_STR = os.getenv("SB_CONN")
if not CONN_STR:
    print("ERROR: Please set SB_CONN environment variable to your Service Bus connection string.")
    sys.exit(1)

def main():
    run_id = str(uuid.uuid4())
    print(f"Using connection string: {CONN_STR}")
    print(f"Target topic: {TOPIC_NAME}")
    print(f"Target subscription: {SUBSCRIPTION_NAME}")
    print("Opening client...")

    with ServiceBusClient.from_connection_string(CONN_STR) as client:
        print("Sending test messages with different message types...")
        with client.get_topic_sender(topic_name=TOPIC_NAME) as sender:
            for msg_type in MESSAGE_TYPES:
                body = f"hello from pub/sub smoke test | run_id={run_id} | type={msg_type}"
                msg = ServiceBusMessage(body)
                msg.application_properties = {"message_type": msg_type}
                sender.send_messages(msg)
                print(f"Sent message with type: {msg_type}")
        print("All messages sent.")

        time.sleep(0.5)

        print("Receiving messages from subscription...")
        received_types = set()
        with client.get_subscription_receiver(
            topic_name=TOPIC_NAME,
            subscription_name=SUBSCRIPTION_NAME,
            max_wait_time=5
        ) as receiver:
            for message in receiver:
                msg_type = message.application_properties.get("message_type")
                text = str(message)
                print(f"Received: {text} | message_type: {msg_type}")
                if run_id in text:
                    received_types.add(msg_type)
                    receiver.complete_message(message)
                else:
                    receiver.complete_message(message)
                    print("Info: received a different message; continuing to look...")
                if received_types == set(MESSAGE_TYPES):
                    print("✅ End-to-end OK (received all message types and completed messages).")
                    return
        print("⚠️ Did not receive all test messages within the wait window.")
        sys.exit(2)

if __name__ == "__main__":
    try:
        main()
    except Exception as ex:
        print(f"❌ Failure: {ex}")
        sys.exit(3)
