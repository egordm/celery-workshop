import multiprocessing
from collections.abc import Iterator


def start_worker(argv: list[str], name_prefix: str = "WORKER") -> None:
    from celery_workshop.celery import app  # noqa: PLC0415

    # Give our process a legible name for logging
    multiprocessing.current_process().name = name_prefix + multiprocessing.current_process().name.replace("Process", "")

    # Configure for single-process worker
    app.conf.update(
        worker_concurrency=1,
        worker_pool="solo",  # Single-threaded execution
    )

    app.worker_main(["--quiet", "worker", "--loglevel=INFO", *argv])


def start_worker_in_process(
    argv: list[str] | None = None, name_prefix: str = "WORKER"
) -> Iterator[multiprocessing.Process]:
    worker_process = multiprocessing.Process(target=start_worker, args=(argv or [], name_prefix))
    worker_process.start()

    try:
        yield worker_process
    finally:
        worker_process.kill()
        worker_process.join(timeout=5)
