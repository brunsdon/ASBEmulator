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

MESSAGE_ID = "DUPLICATE_TEST_ID"

def main():
    print("Sending duplicate messages...")
    with ServiceBusClient.from_connection_string(CONN_STR) as client:
        with client.get_topic_sender(topic_name=TOPIC_NAME) as sender:
            msg1 = ServiceBusMessage("Duplicate test message")
            msg1.message_id = MESSAGE_ID
            msg2 = ServiceBusMessage("Duplicate test message")
            msg2.message_id = MESSAGE_ID
            sender.send_messages([msg1, msg2])
        print("Messages sent.")
        received = 0
        with client.get_subscription_receiver(topic_name=TOPIC_NAME, subscription_name=SUBSCRIPTION_NAME, max_wait_time=5) as receiver:
            for message in receiver:
                print(f"Received: {str(message)} | MessageId: {message.message_id}")
                receiver.complete_message(message)
                received += 1
        if received == 1:
            print("✅ Duplicate detection test passed (only one message received).")
        else:
            print(f"⚠️ Duplicate detection failed (received {received} messages).")
            sys.exit(2)

if __name__ == "__main__":
    try:
        main()
    except Exception as ex:
        print(f"❌ Failure: {ex}")
        sys.exit(3)
