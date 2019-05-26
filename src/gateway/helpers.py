from kombu import Exchange, Queue

def create_queue(**kwargs):
    queue_data = kwargs.get("queue_data")
    exchange_data = kwargs.get("exchange_data")
    return Queue(
        name=queue_data.get("name"),
        exchange=Exchange(name=exchange_data.get('name'), type=exchange_data.get("type")),
        routing_key=queue_data.get("routing_key")
    )