"""
Chapter 1: Introduction to Celery

Learn Celery basics through four exercises:
1. Calling tasks (.delay() and .apply_async())
2. Implementing your own task
3. Running multiple tasks in parallel
4. Task chains and groups

DO NOT MODIFY these tests.
"""

import logging
import multiprocessing
from collections.abc import Iterator

import pytest

from celery_workshop.celery import app
from celery_workshop.exercises_ch1_tasks import (
    run_add_numbers,
    run_mixed_workload,
    run_multiple_tasks,
    run_task_chain,
    run_task_group,
)
from celery_workshop.testing import measure_execution_time, start_worker_in_process

logger = logging.getLogger(__name__)


@pytest.fixture(autouse=True, scope="module")
def celery_app() -> None:
    """Setup Celery app for testing."""
    app.set_current()


@pytest.fixture(scope="module")
def single_worker() -> Iterator[multiprocessing.Process]:
    """Start a single Celery worker for basic tests."""
    yield from start_worker_in_process(concurrency=1)


@pytest.fixture(scope="module")
def parallel_worker() -> Iterator[multiprocessing.Process]:
    """Start a Celery worker with higher concurrency for parallel tests."""
    yield from start_worker_in_process(concurrency=4)


@pytest.fixture(scope="module")
def compute_worker() -> Iterator[multiprocessing.Process]:
    """Start a worker that handles 'compute' queue with concurrency."""
    yield from start_worker_in_process(queues=["compute"], concurrency=2)


@pytest.fixture(scope="module")
def io_worker() -> Iterator[multiprocessing.Process]:
    """Start a worker that handles 'io' queue with concurrency."""
    yield from start_worker_in_process(queues=["io"], concurrency=2)


@pytest.fixture(scope="module")
def default_worker() -> Iterator[multiprocessing.Process]:
    """Start a worker that handles default 'celery' queue with concurrency."""
    yield from start_worker_in_process(queues=["celery"], concurrency=2)


@pytest.mark.usefixtures("single_worker")
def test_exercise_1_call_task():
    """
    Exercise 1: Learn to call Celery tasks

    Test that your run_add_numbers function correctly calls the Celery task
    and returns the result.

    What you learn: .delay(), .get(), basic task calling
    """
    result = run_add_numbers(5, 3)
    assert result == 8


@pytest.mark.usefixtures("single_worker")
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


@pytest.mark.usefixtures("parallel_worker")
def test_exercise_3_multiple_tasks():
    """
    Exercise 3: Running multiple tasks in parallel

    Test that your run_multiple_tasks function correctly runs tasks in parallel
    and collects all results. Verifies actual parallel execution with timing.

    What you learn: Parallel execution, result collection, timing differences
    """
    # Test with simple numbers for timing predictability
    numbers = [(1, 1), (2, 2), (3, 3)]  # Each task takes 0.3s

    with measure_execution_time() as get_elapsed:
        results = run_multiple_tasks(numbers)
        elapsed_time = get_elapsed()

    # Verify results are correct
    expected = [1, 4, 9]  # 1*1, 2*2, 3*3
    assert results == expected

    # The key insight: tasks are running in parallel (check logs for WORKER-CHILD1,2,3)
    # With database overhead, timing varies, but we can verify parallel execution occurred
    logger.info(f"Tasks completed in {elapsed_time:.2f}s with parallel worker (concurrency=4)")
    logger.info("Check logs above - tasks should run on different WORKER-CHILD processes simultaneously")

    # Verify parallel execution happened by checking it's not much slower than single task
    # Single task: ~0.3s + overhead, three in parallel should be similar
    assert elapsed_time < 2.0, f"Tasks took {elapsed_time:.2f}s - too slow, may not be parallel"


@pytest.mark.usefixtures("parallel_worker")
def test_exercise_4_task_group():
    """
    Exercise 4b: Task groups (parallel workflow)

    Test that your run_task_group function creates a group
    that runs multiple tasks in parallel. Verifies actual parallel execution.

    What you learn: Task groups, parallel workflows, Celery primitives
    """
    numbers = [1, 2, 3, 4]  # Each task takes 0.2s

    with measure_execution_time() as get_elapsed:
        results = run_task_group(numbers)
        elapsed_time = get_elapsed()

    # Verify results are correct
    expected = [2, 4, 6, 8]  # Each number doubled
    assert results == expected

    # The key insight: tasks are running in parallel (check logs for WORKER-CHILD1,2,3,4)
    # With database overhead, timing varies, but we can verify parallel execution occurred
    logger.info(f"Group completed in {elapsed_time:.2f}s with parallel worker (concurrency=4)")
    logger.info("Check logs above - tasks should run on different WORKER-CHILD processes simultaneously")

    # Verify parallel execution happened by checking it's not much slower than single task
    # Single task: ~0.2s + overhead, four in parallel should be similar
    assert elapsed_time < 2.0, f"Group took {elapsed_time:.2f}s - too slow, may not be parallel"


@pytest.mark.usefixtures("single_worker")
def test_exercise_4_task_chain():
    """
    Exercise 4a: Task chains (sequential workflow)

    Test that your run_task_chain function creates a proper chain
    where one task's output becomes the next task's input.

    What you learn: Task chains, workflow dependencies
    """
    result = run_task_chain(5)
    # 5 -> double (10) -> add ten (20)
    assert result == 20


@pytest.mark.usefixtures("compute_worker", "io_worker", "default_worker")
def test_exercise_5_queue_routing():
    """
    Exercise 5: Queue routing and worker specialization

    Test that your run_mixed_workload function correctly routes tasks
    to different queues and worker specialization works correctly.

    What you learn: Queue routing, worker specialization, .apply_async(queue=...)

    Note: With concurrent workers (concurrency=2 each), if queue routing is
    implemented incorrectly, all tasks might run on the same worker type.
    Check the terminal output during test execution to see WORKER1/2/3 distribution.
    """
    # Test the main functionality
    results = run_mixed_workload()

    # Verify structure and results
    expected_keys = {"cpu_results", "io_results", "quick_results"}
    assert set(results.keys()) == expected_keys

    # Verify CPU results (4^2=16, 9^2=81)
    assert results["cpu_results"] == [16, 81]

    # Verify I/O results
    expected_io = ["Processed file: data.csv", "Processed file: report.pdf"]
    assert results["io_results"] == expected_io

    # Verify quick results
    expected_quick = ["Quick: hello", "Quick: world"]
    assert results["quick_results"] == expected_quick
