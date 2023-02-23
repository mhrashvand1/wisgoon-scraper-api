from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = 'Displays current time'

    def handle(self, *args, **kwargs):
        if settings.CELERY_BROKER_URL.startswith("amqp"):
            import pika
            credentials = pika.PlainCredentials(
                username=settings.RABBITMQ_USER, 
                password=settings.RABBITMQ_PASS
            )
            try:
                connection = pika.BlockingConnection(
                    pika.ConnectionParameters(
                        host=settings.RABBITMQ_HOST,
                        port=settings.RABBITMQ_PORT,
                        virtual_host=settings.RABBITMQ_VHOST,
                        credentials=credentials
                    )
                )
                connection.close()
            except pika.exceptions.AMQPConnectionError:
                raise Exception("RabbitMQ server is not loaded")
            
        elif settings.CELERY_BROKER_URL.startswith("redis"):
            from redis import Redis
            try:
                r = Redis(
                    host=settings.REDIS_HOST, 
                    port=settings.REDIS_PORT
                )
                r.ping()
            except:
                raise Exception("Redis server is not loaded")
            
        else:
            Exception("Unknown celery brocker url.")
            