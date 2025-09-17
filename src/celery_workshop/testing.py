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


def start_worker(argv: list[str], concurrency: int = 1) -> None:
    from celery_workshop.celery import app

    # Process naming is now handled automatically by Celery app signals

    # Configure worker
    if concurrency == 1:
        app.conf.update(
            worker_concurrency=1,
            worker_pool="solo",  # Single-threaded execution
            worker_prefetch_multiplier=1,  # Process one task at a time
        )
        worker_args = ["--quiet", "worker", "--loglevel=INFO", *argv]
    else:
        app.conf.update(
            worker_concurrency=concurrency,
            worker_prefetch_multiplier=1,  # Important: prevent task hoarding
        )
        worker_args = ["--quiet", "worker", "--loglevel=INFO", f"--concurrency={concurrency}", *argv]

    app.worker_main(worker_args)


def start_worker_in_process(argv: list[str] | None = None, concurrency: int = 1) -> Iterator[multiprocessing.Process]:
    worker_process = multiprocessing.Process(target=start_worker, args=(argv or [], concurrency))
    worker_process.start()

    try:
        yield worker_process
    finally:
        worker_process.kill()
        worker_process.join(timeout=5)
