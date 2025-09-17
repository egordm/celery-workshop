import logging
from typing import Any

from celery import Celery, signals

from celery_workshop.config import basic_celery_config
from celery_workshop.logging import configure_root_logger

# Create Celery app
app = Celery(
    "celery_workshop",
    broker="sqlalchemy+sqlite:///./data/broker.sqlite",
    backend="db+sqlite:///./data/results.sqlite",
)

# Configure for testing
app.conf.update(basic_celery_config)

# Configure task modules to be imported
# Celery app will look in all these modules for @app.task / @shared_task decorated tasks
app.autodiscover_tasks([
    "celery_workshop.case_1_tasks",
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
