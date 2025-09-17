# Celery Workshop 2025

A hands-on workshop for learning Celery distributed task processing.

## What is Celery?

Celery is a **distributed task queue** that lets you run code asynchronously in the background.

**Why use Celery?**
- Long-running tasks don't block your main application
- Background processing (emails, file processing, data analysis)
- Scale across multiple machines easily

## Chapter 1: Celery Basics

Learn through four hands-on exercises:

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

### Exercise 3: Multiple Tasks (Parallel Execution)
Learn to run multiple tasks in parallel by implementing `run_multiple_tasks()`.

```bash
uv run pytest tests/test_chapter_1.py::test_exercise_3_multiple_tasks -v
```

**Documentation**: [Canvas: Primitives](https://docs.celeryq.dev/en/latest/userguide/canvas.html#primitives)

### Exercise 4: Chains and Groups (Workflow Dependencies)
Learn task orchestration by implementing `run_task_chain()` and `run_task_group()`.

```bash
uv run pytest tests/test_chapter_1.py::test_exercise_4_task_chain -v
uv run pytest tests/test_chapter_1.py::test_exercise_4_task_group -v
```

**Documentation**: [Canvas: Chains and Groups](https://docs.celeryq.dev/en/latest/userguide/canvas.html#chains)

## Your Tasks

Open `src/celery_workshop/exercises_ch1_tasks.py` and:

### Task 1: Complete `run_add_numbers()`
Call the provided task and return result.

**What you'll learn**: `.delay()`, `.get()`, basic task calling

### Task 2: Implement `exercise2_greet_user`
Create task that returns "Hello, {name}!"

**What you'll learn**: `@shared_task`, task implementation

### Task 3: Complete `run_multiple_tasks()`
Run multiple tasks in parallel and collect all results.

**What you'll learn**: Parallel execution, result collection

### Task 4a: Complete `run_task_chain()`
Create a chain where tasks run sequentially (output → input).

**What you'll learn**: Task chains, workflow dependencies

### Task 4b: Complete `run_task_group()`
Create a group where tasks run in parallel.

**What you'll learn**: Task groups, parallel workflows

## Run All Tests

```bash
uv run pytest tests/test_chapter_1.py -v
```

## Key Concepts

- **`.delay()`**: Simple task calling
- **`.get()`**: Wait for and retrieve results
- **`@shared_task`**: Create Celery tasks
- **Parallel execution**: Running multiple tasks simultaneously
- **`chain()`**: Sequential task execution (task1 → task2 → task3)
- **`group()`**: Parallel task execution (task1, task2, task3 all at once)

### 🤔 Common Question: Exercise 3 vs Exercise 4b?

Both run tasks in parallel, but with different approaches:

- **Exercise 3** (`run_multiple_tasks`): Manual approach - call `.delay()` multiple times, collect results yourself
- **Exercise 4b** (`run_task_group`): Uses Celery's `group()` primitive - more elegant and optimized

The `group()` approach is preferred for production code as it handles edge cases better and provides better performance.

**Note on Parallel Execution**: The tests automatically start workers with appropriate concurrency. When you see logs showing different `ForkPoolWorker-1`, `ForkPoolWorker-2`, etc., that confirms tasks are running in parallel!

## Additional Resources
- [Celery Introduction](https://docs.celeryq.dev/en/latest/getting-started/introduction.html)