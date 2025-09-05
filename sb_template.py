import os
import sys
import uuid
import time
from dotenv import load_dotenv
from azure.servicebus import ServiceBusClient, ServiceBusMessage

load_dotenv()

# Read connection string from env var
CONN_STR = os.getenv("SB_CONN")
if not CONN_STR:
    print("ERROR: Please set SB_CONN environment variable to your Service Bus connection string.")
    print('Example (Windows):  setx SB_CONN "Endpoint=sb://localhost/;UseDevelopmentEmulator=true;"')
    sys.exit(1)

def main():
    print(f"Using connection string: {CONN_STR}")


    # Create a ServiceBusClient and send/receive a message
    with ServiceBusClient.from_connection_string(CONN_STR) as client:
        # 1) SEND
        print("Sending a test message...")
        with client.get_queue_sender(queue_name=QUEUE_NAME) as sender:
            msg = ServiceBusMessage(body)
            sender.send_messages(msg)
        print("Message sent.")

        # Small delay to allow broker to commit
        time.sleep(0.5)

        # 2) RECEIVE
        print("Receiving message back...")
        with client.get_queue_receiver(queue_name=QUEUE_NAME, max_wait_time=5) as receiver:
            for message in receiver:
                text = str(message)
                print(f"Received: {text}")
                # verify it’s the one we just sent
                if run_id in text:
                    receiver.complete_message(message)
                    print("✅ End-to-end OK (matched run_id and completed message).")
                    return
                else:
                    # Not our message (queue had older messages) — settle and keep looking
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
