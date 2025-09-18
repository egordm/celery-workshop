"""
Simple script to trigger Celery tasks outside of pytest.

Run this after starting workers with:
uv run celery -A celery_workshop.celery worker --loglevel=info
"""

from typing import TYPE_CHECKING

# Import the configured Celery app instead of tasks directly
from celery_workshop.celery import app
from celery_workshop.chapter1 import exercise1_add_numbers

if TYPE_CHECKING:
    from celery.result import AsyncResult


def main():
    """Trigger some tasks and show results."""
    print("🚀 Triggering Celery tasks...")

    app.set_current()

    # Single task
    result = exercise1_add_numbers.delay(10, 20)
    print(f"Task {result.id}: 10 + 20 = {result.get()}")

    # Multiple tasks
    results: list[AsyncResult[int]] = []
    for i in range(3):
        result = exercise1_add_numbers.delay(i, i * 2)
        results.append(result)

    print("Multiple tasks:")
    for result in results:
        print(f"Task {result.id}: result = {result.get()}")

    print("✅ All tasks completed!")


if __name__ == "__main__":
    main()
