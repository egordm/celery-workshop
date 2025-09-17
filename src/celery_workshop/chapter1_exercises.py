"""
Chapter 1: Introduction to Celery Tasks

This file contains exercises for learning Celery basics.
Complete the TODO sections and run the tests to verify your solutions.
"""

from celery import shared_task

from .chapter1 import (
    exercise1_add_numbers,
    exercise3_multiply_numbers,
    exercise4_add_ten,
    exercise4_double_number,
    exercise5_cpu_intensive_task,
    exercise5_io_task,
    exercise5_quick_task,
)

# =============================================================================
# EXERCISE 1: Learn to call tasks
# =============================================================================


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
    import time

    time.sleep(0.1)  # Simulate work
    return f"Hello, {name}!"


# =============================================================================
# EXERCISE 3: Running multiple tasks (parallel execution)
# =============================================================================


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
    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        from celery.result import AsyncResult

    results: list[AsyncResult[int]] = []
    for x, y in numbers:
        result = exercise3_multiply_numbers.delay(x, y)
        results.append(result)

    # Wait for all results
    return [result.get(timeout=10) for result in results]


# =============================================================================
# EXERCISE 4: Orchestrating tasks with chains and groups
# =============================================================================


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


# =============================================================================
# Exercise 5: Queue Routing and Worker Specialization
# =============================================================================


def run_mixed_workload() -> dict[str, list[str] | list[int]]:
    """
    TODO: Run a mixed workload across different queues

    Requirements:
    - Run 2 CPU-intensive tasks (numbers 4, 9) on 'compute' queue
    - Run 2 I/O tasks (files 'data.csv', 'report.pdf') on 'io' queue
    - Run 2 quick tasks (messages 'hello', 'world') on default queue
    - All tasks should run in parallel using different workers
    - Return results organized by queue type

    Hints:
    - Use .apply_async(queue='queue_name') to route tasks to specific queues
    - Collect results and organize them by task type
    - Use timeout when getting results

    NOTE: Queue routing can also be configured globally via Celery settings:
    - task_routes: Maps task names to queues automatically
    - task_queue_ha_policy: High availability settings
    - task_queues: Define available queues and their properties

    Example config-based routing:
    app.conf.task_routes = {
        'exercise5_cpu_intensive_task': {'queue': 'compute'},
        'exercise5_io_task': {'queue': 'io'},
    }

    Expected return format:
    {
        'cpu_results': [16, 81],  # 4^2, 9^2
        'io_results': ['Processed file: data.csv', 'Processed file: report.pdf'],
        'quick_results': ['Quick: hello', 'Quick: world']
    }
    """
    # SOLUTION:

    # Start CPU-intensive tasks on 'compute' queue
    cpu_tasks = [
        exercise5_cpu_intensive_task.apply_async(args=[4], queue="compute"),  # pyright: ignore[reportArgumentType]
        exercise5_cpu_intensive_task.apply_async(args=[9], queue="compute"),  # pyright: ignore[reportArgumentType]
    ]

    # Start I/O tasks on 'io' queue
    io_tasks = [
        exercise5_io_task.apply_async(args=["data.csv"], queue="io"),  # pyright: ignore[reportArgumentType]
        exercise5_io_task.apply_async(args=["report.pdf"], queue="io"),  # pyright: ignore[reportArgumentType]
    ]

    # Start quick tasks on default queue (no queue specified)
    quick_tasks = [exercise5_quick_task.apply_async(args=["hello"]), exercise5_quick_task.apply_async(args=["world"])]  # pyright: ignore[reportArgumentType]

    # Collect results
    cpu_results = [task.get(timeout=10) for task in cpu_tasks]
    io_results = [task.get(timeout=10) for task in io_tasks]
    quick_results = [task.get(timeout=10) for task in quick_tasks]

    return {"cpu_results": cpu_results, "io_results": io_results, "quick_results": quick_results}
