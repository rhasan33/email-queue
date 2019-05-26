import os
from aiohttp import web
from kombu import Connection, Producer, Exchange, Queue
from helpers import create_queue

PIORITY_CONFIG = {
    "high": 9,
    "medium": 5,
    "low": 1
}

# task transporter
def transport_task(key, queue, priority, kwargs={}):
    # payload that will be sent to broker
    payload = {
        'kwargs': kwargs,
    }

    # retry policy for declaring the queue
    retry_policy = {
        'interval_start': 0,
        'interval_step': 2,
        'interval_max': 60,
        'max_retries': 30
    }

    with Connection(os.environ.get('BROKER_URL')) as connection:
        with connection.channel() as channel:
            producer = Producer(channel)
            producer.publish(
                payload,
                retry=True,
                retry_policy=retry_policy,
                exchange=queue.exchange,
                routing_key=queue.routing_key,
                declare=[queue],
                priority=PIORITY_CONFIG[priority]
            )
            producer.release()

async def healthCheck(request):
    return web.json_response({"msg": "queue server up and running"}, status=200)

async def send_email(request):
    body = await request.json()
    data = {
        "to_email": body.get("email"),
        "subject": body.get("subject"),
        "body": body.get("body")
    }
    queue_data = body.get("queue_data")
    exchange_data = body.get("exchange_data")
    email_queue = create_queue(queue_data=queue_data, exchange_data=exchange_data)
    print("queue created")
    transport_task(
        'email-queue',
        email_queue,
        body.get("priority"),
        kwargs=data
    )
    return web.json_response({"msg": "successfully queued"}, status=201)


app = web.Application()
app.add_routes([
    web.get('/', healthCheck),
    web.post('/send-email', send_email),
])