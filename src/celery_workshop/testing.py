import contextlib
import multiprocessing
import time
from collections.abc import Iterator


@contextlib.contextmanager
def measure_execution_time():
    """Context manager to measure execution time."""
    start_time = time.time()
    try:
        yield lambda: time.time() - start_time
    finally:
        pass


def start_worker(argv: list[str] | None = None, concurrency: int = 1, queues: list[str] | None = None) -> None:
    from celery_workshop.celery import app

    # Process naming is now handled automatically by Celery app signals

    # Configure worker through app.conf using multiple update calls
    app.conf.update(worker_concurrency=concurrency)
    app.conf.update(worker_prefetch_multiplier=1)  # Process one task at a time

    # Set pool type based on concurrency
    if concurrency == 1:
        app.conf.update(worker_pool="solo")  # Single-threaded execution

    # Configure task queues if specified
    if queues:
        # Define available queues
        app.conf.update(task_queues={queue: {"exchange": queue, "routing_key": queue} for queue in queues})
        # Set which queues this worker should consume from
        app.conf.update(task_queue_names=queues)

    # Minimal worker args - configuration is handled by app.conf
    worker_args = ["--quiet", "worker", "--loglevel=INFO"]

    # Add any additional arguments
    if argv:
        worker_args.extend(argv)

    app.worker_main(worker_args)


def start_worker_in_process(
    argv: list[str] | None = None, concurrency: int = 1, queues: list[str] | None = None
) -> Iterator[multiprocessing.Process]:
    worker_process = multiprocessing.Process(target=start_worker, args=(argv, concurrency, queues))
    worker_process.start()

    try:
        yield worker_process
    finally:
        worker_process.kill()
        worker_process.join(timeout=5)
