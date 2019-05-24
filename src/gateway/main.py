import os
from aiohttp import web
from kombu import Connection, Producer, Exchange, Queue

PIORITY_CONFIG = {
    "high": 9,
    "medium": 5,
    "low": 1
}

# create exchange and queue
exchange = Exchange('telenor-health', type='direct')
email_queue = Queue(name='email-sending-queue', exchange=exchange, routing_key='send-email')

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
                exchange=exchange,
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