"""
Chapter 1: Introduction to Celery Tasks

This file contains exercises for learning Celery basics.
"""

import time

from celery import shared_task
from celery.result import AsyncResult

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


# =============================================================================
# EXERCISE 3: Running multiple tasks (parallel execution)
# =============================================================================


@shared_task(name="exercise3_multiply_numbers")
def exercise3_multiply_numbers(x: int, y: int) -> int:
    """PROVIDED: Multiplication task for parallel execution patterns"""
    time.sleep(0.3)  # Simulate work
    return x * y


def run_multiple_tasks(numbers: list[tuple[int, int]]) -> list[int]:
    """
    TODO: Run multiple tasks in parallel and collect all results

    Requirements:
    - For each (x, y) tuple in numbers, call exercise3_multiply_numbers.delay(x, y)
    - Collect all result objects in a list
    - Use .get(timeout=10) on each result to get the final values
    - Return list of all results

    Example: numbers = [(2, 3), (4, 5)] should return [6, 20]
    """
    # SOLUTION:
    results: list[AsyncResult[int]] = []
    for x, y in numbers:
        result = exercise3_multiply_numbers.delay(x, y)
        results.append(result)

    # Wait for all results
    return [result.get(timeout=10) for result in results]


# =============================================================================
# EXERCISE 4: Orchestrating tasks with chains and groups
# =============================================================================


@shared_task(name="exercise4_double_number")
def exercise4_double_number(x: int) -> int:
    """PROVIDED: Double a number"""
    time.sleep(0.2)  # Simulate work
    return x * 2


@shared_task(name="exercise4_add_ten")
def exercise4_add_ten(x: int) -> int:
    """PROVIDED: Add ten to a number"""
    time.sleep(0.2)  # Simulate work
    return x + 10


def run_task_chain(number: int) -> int:
    """
    TODO: Create a chain of tasks: double_number -> add_ten

    Requirements:
    - Import: from celery import chain
    - Create a chain that first doubles the number, then adds 10
    - Use chain(task1.s(args), task2.s()) pattern
    - Call .apply_async() on the chain
    - Return the final result with .get(timeout=10)

    Example: number = 5 -> double (10) -> add ten (20)
    """
    # SOLUTION:
    from celery import chain

    workflow = chain(exercise4_double_number.s(number), exercise4_add_ten.s())
    result = workflow.apply_async()
    return result.get(timeout=10)


def run_task_group(numbers: list[int]) -> list[int]:
    """
    TODO: Create a group of tasks that all run in parallel

    Requirements:
    - Import: from celery import group
    - Create a group that doubles each number in the list
    - Use group(task.s(arg) for arg in args) pattern
    - Call .apply_async() on the group
    - Return list of all results with .get(timeout=10)

    Example: numbers = [1, 2, 3] should return [2, 4, 6]

    NOTE: This uses Celery's group() primitive - a more elegant way to run
    multiple tasks in parallel. Compare with run_multiple_tasks() which does
    the same thing manually. group() provides better optimization and can
    handle more complex scenarios like partial failures.
    """
    # SOLUTION:
    from celery import group

    job = group(exercise4_double_number.s(num) for num in numbers)
    result = job.apply_async()
    return result.get(timeout=10)
