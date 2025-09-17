"""
Simple script to trigger Celery tasks outside of pytest.

Run this after starting workers with:
uv run celery -A celery_workshop.celery worker --loglevel=info
"""

from celery_workshop.exercises_ch1_tasks import exercise1_add_numbers


def main():
    """Trigger some tasks and show results."""
    print("🚀 Triggering Celery tasks...")

    # Single task
    result = exercise1_add_numbers.delay(10, 20)
    print(f"Task {result.id}: 10 + 20 = {result.get()}")

    # Multiple tasks
    results = []
    for i in range(3):
        result = exercise1_add_numbers.delay(i, i * 2)
        results.append(result)

    print("Multiple tasks:")
    for result in results:
        print(f"Task {result.id}: result = {result.get()}")

    print("✅ All tasks completed!")


if __name__ == "__main__":
    main()
