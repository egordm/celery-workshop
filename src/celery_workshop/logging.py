import logging


def configure_root_logger():
    # Configure root logger - this is ESSENTIAL
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    # Create console handler with our format
    root_logger.addHandler(create_pretty_print_handler())

    enable_celery_loggers()


def create_pretty_print_handler() -> logging.Handler:
    # Create console handler with our format
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter(
        fmt="[%(asctime)s][%(processName)s][%(levelname)s][%(name)s] %(message)s",
        datefmt="%H:%M:%S",  # This controls the time format!
    )
    handler.setFormatter(formatter)

    return handler


def enable_celery_loggers():
    celery_loggers = [
        "celery",
        "celery.app.trace",  # Task execution logs ("Task xyz succeeded")
        "celery.worker",  # Worker logs
        "celery.task",  # Task logs
    ]

    for logger_name in celery_loggers:
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.INFO)
        logger.propagate = True  # Important: let logs bubble up to root
