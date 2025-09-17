"""
Chapter 1: Introduction to Celery Tasks

This file contains the provided tasks and utilities for the exercises.
Do not modify this file - it's used by the exercises.
"""

import logging
import time

from celery import shared_task

logger = logging.getLogger(__name__)

# =============================================================================
# PROVIDED TASKS
# =============================================================================


@shared_task(name="exercise1_add_numbers")
def exercise1_add_numbers(x: int, y: int) -> int:
    """Simple arithmetic task for learning .delay() and .apply_async()"""
    time.sleep(0.5)  # Simulate work
    return x + y


@shared_task(name="exercise3_multiply_numbers")
def exercise3_multiply_numbers(x: int, y: int) -> int:
    """Multiplication task for parallel execution patterns"""
    time.sleep(0.3)  # Simulate work
    return x * y


@shared_task(name="exercise4_double_number")
def exercise4_double_number(x: int) -> int:
    """Double a number"""
    time.sleep(0.2)  # Simulate work
    return x * 2


@shared_task(name="exercise4_add_ten")
def exercise4_add_ten(x: int) -> int:
    """Add ten to a number"""
    time.sleep(0.2)  # Simulate work
    return x + 10


@shared_task(name="exercise5_cpu_intensive_task")
def exercise5_cpu_intensive_task(number: int) -> int:
    """CPU-intensive task that should run on 'compute' queue"""
    time.sleep(0.5)  # Simulate CPU-intensive work
    result = number**2
    logger.info(f"CPU task: {number}^2 = {result}")
    return result


@shared_task(name="exercise5_io_task")
def exercise5_io_task(filename: str) -> str:
    """I/O task that should run on 'io' queue"""
    time.sleep(0.3)  # Simulate I/O operation
    result = f"Processed file: {filename}"
    logger.info(f"I/O task: {result}")
    return result


@shared_task(name="exercise5_quick_task")
def exercise5_quick_task(message: str) -> str:
    """Quick task that runs on default queue"""
    time.sleep(0.1)  # Quick operation
    result = f"Quick: {message}"
    logger.info(f"Quick task: {result}")
    return result
