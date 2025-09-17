"""
Chapter 1: Introduction to Celery Tasks

This file contains exercises for learning Celery basics.
"""

import time

from celery import shared_task

# =============================================================================
# EXERCISE 1: Learn to call tasks
# =============================================================================


@shared_task(name="exercise1_add_numbers")
def exercise1_add_numbers(x: int, y: int) -> int:
    """PROVIDED: Simple arithmetic task for learning .delay() and .apply_async()"""
    time.sleep(0.5)  # Simulate work
    return x + y


def run_add_numbers(x: int, y: int) -> int:
    """
    TODO: Implement this function to call exercise1_add_numbers task

    Requirements:
    - Call exercise1_add_numbers.delay(x, y)
    - Get the result with .get(timeout=10)
    - Return the result
    """
    # SOLUTION:
    result = exercise1_add_numbers.delay(x, y)
    return result.get(timeout=10)


# =============================================================================
# EXERCISE 2: Implement your own task
# =============================================================================

# TODO: Implement exercise2_greet_user task
# Requirements:
# - Use @shared_task(name="exercise2_greet_user")
# - Takes a name parameter (string)
# - Returns "Hello, {name}!"
# - Add a 0.1 second delay with time.sleep(0.1)


# SOLUTION:
@shared_task(name="exercise2_greet_user")
def exercise2_greet_user(name: str) -> str:
    """Greet a user by name."""
    time.sleep(0.1)  # Simulate work
    return f"Hello, {name}!"
