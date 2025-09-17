import logging
import multiprocessing
from collections.abc import Iterator

import pytest

from celery_workshop.case_1_tasks import add_numbers
from celery_workshop.celery import app
from celery_workshop.testing import start_worker_in_process


@pytest.fixture(autouse=True, scope="module")
def celery_app() -> None:
    app.set_current()


@pytest.fixture(scope="module")
def worker() -> Iterator[multiprocessing.Process]:
    yield from start_worker_in_process()


@pytest.mark.usefixtures("worker")
def test_example():
    logger = logging.getLogger("test_example")
    logger.info("Starting test_example")

    result = add_numbers.delay(4, 6)

    task_result: int = result.get(timeout=None, disable_sync_subtasks=False)

    assert task_result == 10


@pytest.mark.usefixtures("worker")
def test_example2():
    result = add_numbers.delay(4, 6)

    task_result: int = result.get(timeout=None, disable_sync_subtasks=False)

    assert task_result == 10
