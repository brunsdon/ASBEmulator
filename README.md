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
### Test Scripts and Details

#### sb_queue_smoke_test.py
Sends a message to a queue and verifies it can be received and completed. Use this to check basic queue functionality and connectivity.

#### sb_topic_smoke_test.py
Sends a message to a topic and verifies it can be received from a subscription. Use this to check basic topic/subscription functionality and connectivity.

#### sb_topic_dynamic_smoke_test.py
Attempts to create topics and subscriptions in code using the Azure SDK. Only works with real Azure Service Bus, not the emulator. Use to validate management API integration.

#### sb_pubsub_smoke_test.py
Sends messages with different types in the header to a topic, and receives them from a single subscription. Demonstrates pub/sub filtering by message type in code.

#### sb_large_message_test.py
Sends and receives a large message (near max size) to test emulator limits and error handling. Useful for validating message size constraints.

#### sb_batch_test.py
Sends and receives a batch of messages to test throughput, ordering, and batch API support.

#### sb_deadletter_test.py
Sends a message and intentionally does not complete it, causing it to exceed max delivery count and move to the dead-letter queue. Verifies dead-letter queue handling and error scenarios.

#### sb_duplicate_test.py
Sends two messages with the same MessageId to test duplicate detection. Only one should be received if duplicate detection is enabled in config.

#### sb_concurrent_consumer_test.py
Starts multiple consumers on the same subscription to test concurrent message processing and load balancing. Useful for scaling scenarios.

#### sb_delayed_delivery_test.py
Schedules a message for future delivery and verifies it is received at the correct time. Tests support for scheduled (delayed) messages.

### Queue Smoke Test

Sends a message to a queue and verifies it can be received and completed. Use this to check basic queue functionality and connectivity.

```bash
python sb_queue_smoke_test.py
```

### Topic Smoke Test

Sends a message to a topic and verifies it can be received from a subscription. Use this to check basic topic/subscription functionality and connectivity.
### Test Coverage Summary

| Script                        | Purpose                                                      | Emulator Support |
|-------------------------------|--------------------------------------------------------------|------------------|
| sb_queue_smoke_test.py        | Basic queue send/receive                                     | Yes              |
| sb_topic_smoke_test.py        | Basic topic/subscription send/receive                        | Yes              |
| sb_topic_dynamic_smoke_test.py| Dynamic topic/sub creation (SDK)                             | No               |
| sb_pubsub_smoke_test.py       | Pub/sub with message type filtering                          | Yes              |
| sb_large_message_test.py      | Send/receive large message                                   | Yes              |
| sb_batch_test.py              | Batch send/receive                                           | Yes              |
| sb_deadletter_test.py         | Dead-letter queue handling                                   | Yes              |
| sb_duplicate_test.py          | Duplicate detection                                          | Yes              |
| sb_concurrent_consumer_test.py| Multiple consumers on one subscription                       | Yes              |
| sb_delayed_delivery_test.py   | Scheduled (delayed) message delivery                         | Yes (if supported)|


```bash
python sb_topic_smoke_test.py
```

### Dynamic Topic Smoke Test


Attempts to create topics and subscriptions in code using the Azure SDK. Only works with real Azure Service Bus, not the emulator. Use to validate management API integration.

```bash
python sb_topic_dynamic_smoke_test.py
```

> **Note:** This test will fail when using the Service Bus Emulator, as the emulator does not support management operations (topic/subscription creation) via the SDK. Use this test only against real Azure Service Bus. For emulator, define all entities in `config.json` before starting.



### Pub/Sub Smoke Test

Sends messages with different types in the header to a topic, and receives them from a single subscription. Demonstrates pub/sub filtering by message type in code.
Sends and receives a large message (near max size) to test emulator limits and error handling. Useful for validating message size constraints.
Sends and receives a batch of messages to test throughput, ordering, and batch API support.
Sends a message and intentionally does not complete it, causing it to exceed max delivery count and move to the dead-letter queue. Verifies dead-letter queue handling and error scenarios.
Sends two messages with the same MessageId to test duplicate detection. Only one should be received if duplicate detection is enabled in config.
Starts multiple consumers on the same subscription to test concurrent message processing and load balancing. Useful for scaling scenarios.
Schedules a message for future delivery and verifies it is received at the correct time. Tests support for scheduled (delayed) messages.

```bash

python sb_pubsub_smoke_test.py
```

This test uses the `pubsub.topic` and `pubsub.subscription` defined in your config. Messages are sent with a `message_type` property in the header and received from the single subscription.


## Troubleshooting


### Topic or Subscription Not Found

If you see errors like:

```
❌ Failure: The messaging entity 'sb://.../pubsub.topic' could not be found.

```

Check the following:

- Ensure the topic and subscription are defined in `config.json`.
- Stop and restart the emulator after making changes to `config.json` so it reloads the configuration.
- Confirm the names in your test script match those in the config exactly.


Example restart command (from your project directory):

```powershell
docker compose down
docker compose up -d
```


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

## Service Bus Emulator Limitations

The Service Bus Emulator is useful for local development, but it does not fully replicate all features of Azure Service Bus. Key limitations include:

- **Management Operations:** You cannot create, update, or delete topics, queues, or subscriptions via the Azure SDK. All entities must be defined in `config.json` before starting the emulator.
- **Rules and Filters:** Advanced subscription rules and SQL filters may not be supported. All messages are delivered to the subscription unless filtered by your application code.
- **Sessions:** Session-based messaging may not be supported or may have limited functionality.
- **Partitioning:** Partitioned entities are not supported.
- **Geo-DR and Availability:** No support for geo-replication, disaster recovery, or availability zones.
- **Authorization:** Only basic authentication is supported; advanced RBAC and claims-based access are not available.
- **Message Size:** Maximum message size may differ from Azure Service Bus (typically 256KB for Standard, 1MB for Premium in Azure).
- **Duplicate Detection:** May not behave identically to Azure; test thoroughly if your solution relies on this feature.
- **Scheduled Delivery:** Scheduled (delayed) messages may not be supported or may have limited reliability.
- **Dead-Lettering:** Dead-letter queue behavior may differ, especially for unsupported features.
- **Auto-Forwarding:** Forwarding messages between entities may not be available.
- **Diagnostics and Monitoring:** Limited support for metrics, logging, and diagnostics compared to Azure.
- **Service Limits:** Throughput, concurrency, and scaling are limited compared to cloud service.

> Always consult the emulator documentation for the most up-to-date list of supported and unsupported features. For production scenarios, validate all critical features against real Azure Service Bus.



