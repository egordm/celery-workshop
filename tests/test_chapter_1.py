"""
Chapter 1: Introduction to Celery

Learn Celery basics through two exercises:
1. Calling tasks (.delay() and .apply_async())
2. Implementing your own task

DO NOT MODIFY these tests.
"""

import multiprocessing
from collections.abc import Iterator

import pytest

from celery_workshop.celery import app
from celery_workshop.exercises_ch1_tasks import run_add_numbers
from celery_workshop.testing import start_worker_in_process


@pytest.fixture(autouse=True, scope="module")
def celery_app() -> None:
    """Setup Celery app for testing."""
    app.set_current()


@pytest.fixture(scope="module")
def worker() -> Iterator[multiprocessing.Process]:
    """Start a Celery worker in background for testing."""
    yield from start_worker_in_process()


@pytest.mark.usefixtures("worker")
def test_exercise_1_call_task():
    """
    Exercise 1: Learn to call Celery tasks

    Test that your run_add_numbers function correctly calls the Celery task
    and returns the result.

    What you learn: .delay(), .get(), basic task calling
    """
    result = run_add_numbers(5, 3)
    assert result == 8


@pytest.mark.usefixtures("worker")
def test_exercise_2_implement_task():
    """
    Exercise 2: Implement your own Celery task

    Test that you implemented exercise2_greet_user correctly.

    What you learn: @shared_task, task implementation
    """
    try:
        from celery_workshop.exercises_ch1_tasks import exercise2_greet_user

        result = exercise2_greet_user.delay("Alice")
        task_result = result.get(timeout=5)
        assert task_result == "Hello, Alice!"

    except ImportError:
        pytest.skip("Exercise 2 not implemented yet")
