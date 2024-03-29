import os
from aiohttp import web
from kombu import Connection, Producer, Exchange, Queue
from helpers.helpers import invoice_queue
from middlewares.middlewares import authentication, validation, response_handler

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
        "customer": body.get("customer"),
        "order_number": body.get("order_number"),
        "items": body.get("items"),
        "delivery_fee": body.get("delivery_fee"),
        "bcc": body.get("bcc", []),
    }
    email_queue = invoice_queue()
    transport_task(
        'email-queue',
        email_queue,
        body.get("priority"),
        kwargs=data
    )
    return web.HTTPCreated(text="queue created successfully.")


app = web.Application(middlewares=[response_handler, authentication, validation])
app.add_routes([
    web.get('/', healthCheck),
    web.post('/api/send-invoice', send_email),
])