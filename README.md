# Celery Workshop 2025

A hands-on workshop for learning Celery distributed task processing.

## What is Celery?

Celery is a **distributed task queue** that lets you run code asynchronously in the background.

**Why use Celery?**
- Long-running tasks don't block your main application
- Background processing (emails, file processing, data analysis)
- Scale across multiple machines easily

## Chapter 1: Celery Basics

Learn through two hands-on exercises:

### Exercise 1: Call a Task
Learn to use `.delay()` and `.apply_async()` by implementing `run_add_numbers()`.

```bash
uv run pytest tests/test_chapter_1.py::test_exercise_1_call_task -v
```

**Documentation**: [Calling Tasks](https://docs.celeryq.dev/en/latest/userguide/calling.html)

### Exercise 2: Create a Task  
Implement your own `exercise2_greet_user` task with `@shared_task`.

```bash
uv run pytest tests/test_chapter_1.py::test_exercise_2_implement_task -v
```

**Documentation**: [Creating Tasks](https://docs.celeryq.dev/en/latest/userguide/tasks.html)

## Your Tasks

Open `src/celery_workshop/exercises_ch1_tasks.py` and:

### Task 1: Complete `run_add_numbers()`
Call the provided task and return result.

**What you'll learn**: `.delay()`, `.get()`, basic task calling

### Task 2: Implement `exercise2_greet_user`
Create task that returns "Hello, {name}!"

**What you'll learn**: `@shared_task`, task implementation

## Run All Tests

```bash
uv run pytest tests/test_chapter_1.py -v
```

## Key Concepts

- **`.delay()`**: Simple task calling
- **`.get()`**: Wait for and retrieve results
- **`@shared_task`**: Create Celery tasks

## Additional Resources
- [Celery Introduction](https://docs.celeryq.dev/en/latest/getting-started/introduction.html)