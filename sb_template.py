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
    print('Example (Windows):  set SB_CONN "Endpoint=sb://localhost/;UseDevelopmentEmulator=true;"')
    sys.exit(1)

def main():
    print(f"Using connection string: {CONN_STR}")

    sys.exit(2)

if __name__ == "__main__":
    try:
        main()
    except Exception as ex:
        print(f"❌ Failure: {ex}")
        sys.exit(3)
