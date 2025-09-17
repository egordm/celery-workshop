import multiprocessing

import pytest

from celery_workshop.logging import configure_root_logger


@pytest.fixture(scope="session", autouse=True)
def setup_logging():
    multiprocessing.current_process().name = "SCHEDULER"

    configure_root_logger()
