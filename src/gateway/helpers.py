from kombu import Exchange, Queue

def invoice_queue(**kwargs):
    queue_data = {
		"name": "invoice_queue",
		"routing_key": "invoice"
    }
    exchange_data = {
		"name": "telenor-health",
		"type": "direct"
	}
    return Queue(
        name=queue_data.get("name"),
        exchange=Exchange(name=exchange_data.get('name'), type=exchange_data.get("type")),
        routing_key=queue_data.get("routing_key")
    )