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

Both scripts require the `SB_CONN` environment variable to be set to your Service Bus connection string.

Example (Windows):

```powershell
setx SB_CONN "Endpoint=sb://localhost/;UseDevelopmentEmulator=true;"
```

## References

- https://learn.microsoft.com/en-us/azure/service-bus-messaging/overview-emulator
- https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/servicebus/azure-servicebus
- https://learn.microsoft.com/en-us/python/api/overview/azure/servicebus-readme?view=azure-python
- https://app.pluralsight.com/library/courses/azure-service-bus-in-depth/table-of-contents



