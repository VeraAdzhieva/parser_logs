import os
import sys

import structlog


def setup_logging(syslog_file_path: str | None) -> None:
    """
    Настраивает structlog для записи в файл или stdout.
    """
    processors = [
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.dict_tracebacks,
        structlog.processors.JSONRenderer(ensure_ascii=False),
    ]

    # Если указан путь к файлу — настраиваем запись в файл
    if syslog_file_path:
        log_dir = os.path.dirname(syslog_file_path)
        if log_dir:
            os.makedirs(log_dir, exist_ok=True)

        file = open(syslog_file_path, "a", encoding="utf-8")

        structlog.configure(
            processors=processors,
            logger_factory=structlog.PrintLoggerFactory(file),
            cache_logger_on_first_use=False,
        )
    else:
        # Запись в stdout
        structlog.configure(
            processors=processors,
            logger_factory=structlog.PrintLoggerFactory(sys.stdout),
            cache_logger_on_first_use=False,
        )
