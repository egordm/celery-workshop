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

### Exercise 2: Create a Task  
Implement your own `exercise2_greet_user` task with `@shared_task`.

```bash
uv run pytest tests/test_chapter_1.py::test_exercise_2_implement_task -v
```

## Your Tasks

Open `src/celery_workshop/exercises_ch1_tasks.py` and:

1. **Complete `run_add_numbers()`** - Call the provided task and return result
2. **Implement `exercise2_greet_user`** - Create task that returns "Hello, {name}!"

## Run All Tests

```bash
uv run pytest tests/test_chapter_1.py -v
```

## Key Concepts

- **`.delay()`**: Simple task calling
- **`.get()`**: Wait for and retrieve results
- **`@shared_task`**: Create Celery tasks

## Documentation
- [Celery Introduction](https://docs.celeryq.dev/en/latest/getting-started/introduction.html)
- [Calling Tasks](https://docs.celeryq.dev/en/latest/userguide/calling.html)