import os
import sys
import threading
from dotenv import load_dotenv
from azure.servicebus import ServiceBusClient, ServiceBusMessage

load_dotenv()
TOPIC_NAME = "pubsub.topic"
SUBSCRIPTION_NAME = "pubsub.subscription"
CONN_STR = os.getenv("SB_CONN")
if not CONN_STR:
    print("ERROR: Please set SB_CONN environment variable to your Service Bus connection string.")
    sys.exit(1)

NUM_CONSUMERS = 2
NUM_MESSAGES = 4

def consumer_thread(thread_id):
    with ServiceBusClient.from_connection_string(CONN_STR) as client:
        with client.get_subscription_receiver(topic_name=TOPIC_NAME, subscription_name=SUBSCRIPTION_NAME, max_wait_time=5) as receiver:
            for message in receiver:
                print(f"Thread {thread_id} received: {str(message)}")
                receiver.complete_message(message)

def main():
    print("Sending messages for concurrent consumer test...")
    with ServiceBusClient.from_connection_string(CONN_STR) as client:
        with client.get_topic_sender(topic_name=TOPIC_NAME) as sender:
            for i in range(NUM_MESSAGES):
                sender.send_messages(ServiceBusMessage(f"Concurrent test message {i}"))
    print("Messages sent. Starting consumers...")
    threads = [threading.Thread(target=consumer_thread, args=(i,)) for i in range(NUM_CONSUMERS)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    print("✅ Concurrent consumer test completed.")

if __name__ == "__main__":
    try:
        main()
    except Exception as ex:
        print(f"❌ Failure: {ex}")
        sys.exit(3)
