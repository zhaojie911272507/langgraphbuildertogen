from loguru import logger as loguru_logger
import logging
import sys
from datetime import datetime
from functools import wraps


# Singleton decorator to ensure the logger is initialized only once
def singleton(fn):
    has_run = False

    @wraps(fn)
    def wrapper(*args, **kwargs):
        nonlocal has_run
        if not has_run:
            result = fn(*args, **kwargs)
            has_run = True
            return result

    return wrapper


@singleton
def initialize_logger():
    """Initialize the logger with a datetime-based log file name and configure the log format."""
    log_filename = datetime.now().strftime("app_%Y%m%d_%H%M%S.log")
    log_path = f"/tmp/logs/{log_filename}"

    # Adjust log format to explicitly include trace_id
    log_format = (
        '{time:YYYY-MM-DD HH:mm:ss} {level} trace_id={extra[details][trace_id]} {message}'
    )

    # Log to file and stdout
    loguru_logger.add(log_path, rotation="500 MB", format=log_format, level="INFO", serialize=True)
    loguru_logger.add(sys.stdout, format=log_format, level="INFO", serialize=True)

    # Integrate with the Python logging module
    class InterceptHandler(logging.Handler):
        def emit(self, record):
            logger_opt = loguru_logger.opt(depth=6, exception=record.exc_info)
            logger_opt.log(record.levelname.lower(), record.getMessage())

    logging.basicConfig(handlers=[InterceptHandler()], level=logging.INFO)
    logging.getLogger().handlers = [InterceptHandler()]

    # Use % style format for logging to stdout to avoid ValueError
    # log_handler = logging.StreamHandler(sys.stdout)  # Stream handler for logging output
    # log_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))  # % style format
    # logging.getLogger().addHandler(log_handler)  # Add stream handler to the global logger


# Initialize the logger (this will be done only once due to the singleton decorator)
initialize_logger()


def log_with_trace_id(message, trace_id="N/A", level="INFO", open_trace_id=True):
    """
    Log a message with a mandatory trace_id. Supports different log levels.

    Args:
        message (str): The log message.
        trace_id (str): A unique identifier for tracing logs.
        level (str): The log level (e.g., "INFO", "ERROR", "WARNING").

    Raises:
        ValueError: If trace_id is missing or None.
    """
    if not trace_id and open_trace_id == True:
        loguru_logger.bind(details={"trace_id": "N/A"}).error("Missing trace_id for message: {message}")
        raise ValueError("The 'trace_id' parameter is required but was not provided.")

    # Bind trace_id and log the message at the specified level
    bound_logger = loguru_logger.bind(details={"trace_id": trace_id})

    if level.upper() == "INFO":
        bound_logger.info(message)
    elif level.upper() == "ERROR":
        bound_logger.error(message)
    elif level.upper() == "WARNING":
        bound_logger.warning(message)
    elif level.upper() == "DEBUG":
        bound_logger.debug(message)
    else:
        bound_logger.info(f"Unknown log level '{level}', defaulting to INFO: {message}")


# Patch the log_with_trace_id function to logger
loguru_logger.patch(lambda self: setattr(self, "log_with_trace_id", log_with_trace_id))
