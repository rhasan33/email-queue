import os
from time import sleep
from celery import Celery, bootsteps
from kombu import Consumer, Exchange, Queue
import logging
from .send_email import mailer

logger = logging.getLogger(__name__)

exchange = Exchange('telenor-health', type='direct')
email_queue = Queue(name='invoice_queue', exchange=exchange, routing_key='invoice')

celery_app = Celery(
    'consumer',
    broker=os.environ.get('CELERY_BROKER_URL'),
    backend=os.environ.get('CELERY_BROKER_URL')
)


class EmailConsumer(bootsteps.ConsumerStep):
    def get_consumers(self, channel):
        return [Consumer(channel,
                         queues=[email_queue],
                         callbacks=[self.handle_message],
                         accept=['json'])]

    def handle_message(self, body, message):
        data = body.get("kwargs")
        mailer(
            data.get("customer"),
            data.get("order_number"),
            data.get("items"),
            data.get("delivery_fee"),
            data.get("bcc"),
        )
        logger.info(data.get("bcc"))
        logger.info("email sent.")
        message.ack()

celery_app.steps['consumer'].add(EmailConsumer)


if __name__ == '__main__':
    celery_app.start()
