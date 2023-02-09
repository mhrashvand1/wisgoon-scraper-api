from django.core.management.base import BaseCommand
from config.settings import CELERY_BROKER_URL


class Command(BaseCommand):
    help = 'Displays current time'

    def handle(self, *args, **kwargs):
        if CELERY_BROKER_URL.startswith("amqp"):
            from config.settings import (
                RABBITMQ_USER,
                RABBITMQ_PASS,
                RABBITMQ_VHOST,
                RABBITMQ_HOST,
                RABBITMQ_PORT,
            )
            import pika
            credentials = pika.PlainCredentials(username=RABBITMQ_USER, password=RABBITMQ_PASS)
            try:
                connection = pika.BlockingConnection(
                    pika.ConnectionParameters(
                        host=RABBITMQ_HOST,
                        port=RABBITMQ_PORT,
                        virtual_host=RABBITMQ_VHOST,
                        credentials=credentials
                    )
                )
                connection.close()
            except pika.exceptions.AMQPConnectionError:
                raise Exception("RabbitMQ server is not loaded")
            
        elif CELERY_BROKER_URL.startswith("redis"):
            from config.settings import REDIS_HOST, REDIS_PORT
            from redis import Redis
            try:
                r = Redis(host=REDIS_HOST, port=REDIS_PORT)
                r.ping()
            except:
                raise Exception("Redis server is not loaded")
            
        else:
            Exception("Unknown celery brocker url.")
            