import logging
import multiprocessing
from typing import Any

from celery import Celery, signals

from celery_workshop.config import basic_celery_config
from celery_workshop.logging import configure_root_logger

# Create Celery app
app = Celery(
    "celery_workshop",
    broker="sqlalchemy+sqlite:///./data/broker.sqlite",
    backend="db+sqlite:///./data/backend.sqlite",
)

# Configure for testing
app.conf.update(basic_celery_config)

# Configure task modules to be imported
# Celery app will look in all these modules for @app.task / @shared_task decorated tasks
app.autodiscover_tasks([
    "celery_workshop.chapter1",
    "celery_workshop.chapter1_exercises",
])


@signals.setup_logging.connect()
def setup_celery_logging(**kwargs: dict[str, Any]):
    _ = kwargs  # Unused
    configure_root_logger()


@signals.after_setup_logger.connect()
def after_setup_celery_logger(logger: logging.Logger, *args: list[Any], **kwargs: dict[str, Any]):
    """Fine-tune after Celery sets up its loggers"""
    _ = args, kwargs  # Unused
    logger.propagate = True
    logger.setLevel(logging.INFO)


@signals.worker_init.connect()
def setup_main_worker_process_name(**_kwargs: dict[str, Any]) -> None:
    """Give main worker process a readable name."""
    current_process = multiprocessing.current_process()
    if "Process" in current_process.name:
        # Handle both "Process-1" and "Process" patterns
        current_process.name = current_process.name.replace("Process-", "WORKER").replace("Process", "WORKER")


@signals.worker_ready.connect()
def setup_main_worker_process_name_fallback(**_kwargs: dict[str, Any]) -> None:
    """Give main worker process a readable name."""
    current_process = multiprocessing.current_process()
    if "Process" in current_process.name:
        current_process.name = current_process.name.replace("Process-", "WORKER").replace("Process", "WORKER")


@signals.worker_process_init.connect()
def setup_worker_child_process_name(**_kwargs: dict[str, Any]) -> None:
    """Rename worker child processes for better logging."""
    current_process = multiprocessing.current_process()
    # Extract worker number from original name (e.g., "ForkPoolWorker-1" -> "1")
    if "PoolWorker-" in current_process.name:
        worker_num = current_process.name.split("-")[-1]
        current_process.name = f"WORKER-CHILD{worker_num}"
