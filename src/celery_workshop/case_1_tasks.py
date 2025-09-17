import time

from celery import shared_task
from celery.utils.log import get_task_logger


@shared_task(name="add_numbers")
def add_numbers(x: int, y: int) -> int:
    """Simple test task"""
    logger = get_task_logger(__name__)

    logger.info(f"Adding {x} + {y}")
    time.sleep(0.1)  # Simulate some work
    return x + y


@shared_task(name="multiply_numbers")
def multiply_numbers(x: int, y: int) -> int:
    """Another test task"""
    return x * y
