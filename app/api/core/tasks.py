from celery import shared_task
from core.utils import run_crawler


@shared_task
def run_crawler_task(username, from_datetime=None):
    run_crawler(username, from_datetime)
    return f"Page {username} has been crawled"