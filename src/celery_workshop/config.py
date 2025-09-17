# https://docs.celeryq.dev/en/latest/userguide/configuration.html
basic_celery_config = {
    "task_always_eager": False,  # If True, tasks will be executed locally by blocking until the task returns
    "task_eager_propagates": True,  # If True, exceptions raised by tasks will propagate to the caller
    "task_store_eager_result": True,  # If True, results of eager tasks will be stored
    # Serialize tasks and results as JSON
    "task_serializer": "json",
    "accept_content": ["json"],
    "result_serializer": "json",
    "result_expires": 3600,  # Expiration time for task results (in seconds)
    "timezone": "UTC",  # Timezone for the application
    "enable_utc": True,  # Enable UTC timezone
    "worker_hijack_root_logger": False,  # Crucial: don't let Celery hijack logging
    "worker_log_format": "%(asctime)s - %(name)s - %(levelname)s - [%(processName)s] %(message)s",
    "worker_task_log_format": "%(asctime)s - %(name)s - %(levelname)s - [%(processName)s] %(message)s",
}
