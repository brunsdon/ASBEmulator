# Service Bus and SB Emulator

**Put together python scripts to show potential of SB Emulator with Azure Service Bus Client for development**

## Installation

**[Azure Service Bus client library for Python](https://pypi.org/project/azure-servicebus/):**
```bash
pip install azure-servicebus
```

**[python-dotenv](https://pypi.org/project/python-dotenv/):**
```bash
pip install python-dotenv
```

**Deploy to Docker:**
```bash
docker compose up -d
```

## Configuration

Edit `config.json` to define queues, topics, and subscriptions. Example for topic:

> **Note:** The Service Bus Emulator does not support management operations (such as creating topics or subscriptions) via the Azure SDK. All topics and subscriptions must be defined in `config.json` and created when the emulator starts. Dynamic creation in code will fail with connection errors.

```json
"Topics": [
	{
		"Name": "topic.1",
		"Properties": {
			"DefaultMessageTimeToLive": "PT1H",
			"DuplicateDetectionHistoryTimeWindow": "PT20S",
			"RequiresDuplicateDetection": false
		},
		"Subscriptions": [
			{
				"Name": "subscription.1",
				"Properties": {
					"LockDuration": "PT1M",
					"MaxDeliveryCount": 3,
					"DefaultMessageTimeToLive": "PT1H",
					"DeadLetteringOnMessageExpiration": false
				}
			}
		]
	}
]
```

## Smoke Tests

### Queue Smoke Test

Run the queue smoke test to verify end-to-end messaging:

```bash
python sb_queue_smoke_test.py
```

### Topic Smoke Test

Run the topic smoke test to verify topic and subscription messaging:

```bash
python sb_topic_smoke_test.py
```

### Dynamic Topic Smoke Test

`sb_topic_dynamic_smoke_test.py` attempts to create topics and subscriptions in code using the Azure SDK:

```bash
python sb_topic_dynamic_smoke_test.py
```

> **Note:** This test will fail when using the Service Bus Emulator, as the emulator does not support management operations (topic/subscription creation) via the SDK. Use this test only against real Azure Service Bus. For emulator, define all entities in `config.json` before starting.

## Environment Variables

The Service Bus connection string should be set in the `.env` file as follows:

```
SB_CONN="Endpoint=sb://localhost/;UseDevelopmentEmulator=true;"
```

This will be loaded automatically by the smoke test scripts. You can also set it as a system environment variable if preferred.

## References

- https://learn.microsoft.com/en-us/azure/service-bus-messaging/overview-emulator
- https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/servicebus/azure-servicebus
- https://learn.microsoft.com/en-us/python/api/overview/azure/servicebus-readme?view=azure-python
- https://app.pluralsight.com/library/courses/azure-service-bus-in-depth/table-of-contents



