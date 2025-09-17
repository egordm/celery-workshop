# Celery Workshop 2025

A hands-on workshop for learning Celery distributed task processing.

## What is Celery?

Celery is a **distributed task queue** that lets you run code asynchronously in the background.

**Why use Celery?**
- Long-running tasks don't block your main application
- Background processing (emails, file processing, data analysis)
- Scale across multiple machines easily

## Chapter 1: Celery Basics

Open `src/celery_workshop/exercises_ch1_tasks.py` and complete five hands-on exercises:

### Exercise 1: Call a Task
**Task**: Complete `run_add_numbers()` - call the provided task and return result.

**What you'll learn**: `.delay()`, `.get()`, basic task calling

```bash
uv run pytest tests/test_chapter_1.py::test_exercise_1_call_task -v
```

**Documentation**: [Calling Tasks](https://docs.celeryq.dev/en/latest/userguide/calling.html)

### Exercise 2: Create a Task  
**Task**: Implement `exercise2_greet_user` task that returns "Hello, {name}!"

**What you'll learn**: `@shared_task`, task implementation

```bash
uv run pytest tests/test_chapter_1.py::test_exercise_2_implement_task -v
```

**Documentation**: [Creating Tasks](https://docs.celeryq.dev/en/latest/userguide/tasks.html)

### Exercise 3: Multiple Tasks (Parallel Execution)
**Task**: Complete `run_multiple_tasks()` - run multiple tasks in parallel and collect all results.

**What you'll learn**: Parallel execution, result collection

```bash
uv run pytest tests/test_chapter_1.py::test_exercise_3_multiple_tasks -v
```

**Documentation**: [Canvas: Primitives](https://docs.celeryq.dev/en/latest/userguide/canvas.html#primitives)

### Exercise 4: Chains and Groups (Workflow Dependencies)
**Tasks**: 
- Complete `run_task_chain()` - create a chain where tasks run sequentially (output → input)
- Complete `run_task_group()` - create a group where tasks run in parallel

**What you'll learn**: Task chains, task groups, workflow dependencies, parallel workflows

```bash
uv run pytest tests/test_chapter_1.py::test_exercise_4_task_chain -v
uv run pytest tests/test_chapter_1.py::test_exercise_4_task_group -v
```

**Documentation**: [Canvas: Chains and Groups](https://docs.celeryq.dev/en/latest/userguide/canvas.html#chains)

### Exercise 5: Queue Routing (Worker Specialization)
**Task**: Complete `run_mixed_workload()` - route different tasks to different queues (compute, io, default).

**What you'll learn**: Queue routing, worker specialization, `apply_async(queue=...)`

```bash
uv run pytest tests/test_chapter_1.py::test_exercise_5_queue_routing -v
```

**Two approaches for queue routing:**
1. **Manual routing**: `task.apply_async(queue='compute')` (used in this exercise)
2. **Config-based routing**: Set `app.conf.task_routes` for automatic routing

**Documentation**: [Routing Tasks](https://docs.celeryq.dev/en/latest/userguide/routing.html)

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

**Note on Parallel Execution**: The tests automatically start workers with appropriate concurrency. When you see logs showing different `WORKER-CHILD-1`, `WORKER-CHILD-2`, etc., that confirms tasks are running in parallel!

## Additional Resources
- [Celery Introduction](https://docs.celeryq.dev/en/latest/getting-started/introduction.html)