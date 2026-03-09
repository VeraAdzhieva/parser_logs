import gzip
import os
import re
from datetime import datetime
from typing import IO, Any

import structlog

import src.statistics as statisticsFile

structlog.configure()
logger = structlog.get_logger()

# Шаблон лога
NGINX_LOG_PATTERN = re.compile(
    r"(?P<remote_addr>\d+\.\d+\.\d+\.\d+)\s+"
    r"(?P<remote_user>\S+)\s+"
    r"(?P<http_x_real_ip>\S+)\s+"
    r"\[(?P<time_local>[^\]]+)\]\s+"
    r'"(?P<request>[^"]*)"\s+'
    r"(?P<status>\d+)\s+"
    r"(?P<body_bytes_sent>\d+)\s+"
    r'"(?P<http_referer>[^"]*)"\s+'
    r'"(?P<http_user_agent>[^"]*)"\s+'
    r'"(?P<http_x_forwarded_for>[^"]*)"\s+'
    r'"(?P<requesthttp_X_REQUEST_ID_id>[^"]*)"\s+'
    r'"(?P<http_X_RB_USER>[^"]*)"\s*'
    r"(?P<request_time>\d+\.\d+)?"
)


# Получает последний файл по последней дате в названии и только логи nginx
def get_last_logfile(config: dict) -> tuple:
    if not config.get("LOG_DIR"):
        raise Exception("Не указана директория логов")

    if not config.get("TEMPLATE_FILENAME"):
        raise Exception("Не указан шаблон имени файла логов")

    log_dir = config.get("LOG_DIR")
    template_name = config.get("TEMPLATE_FILENAME")

    if not log_dir:
        raise Exception("Пустое значение конфига LOG_DIR")

    if not os.path.exists(log_dir):
        #  logger.error("Директория %s не найдена", log_dir)
        raise Exception("Директория %s не найдена", log_dir)

    latest_file = None
    latest_date = datetime.min

    for filename in os.listdir(log_dir):
        filepath = os.path.join(log_dir, filename)

        if not os.path.isfile(filepath) or template_name not in filename:
            logger.info(" %s не является файлом или не nginx", filename)
            continue

        match = re.search(r"(\d{8})", filename)
        if not match:
            logger.info(" %s - у файла не указана дата", filename)
            continue

        date_str = match.group(1)

        try:
            file_date = datetime.strptime(date_str, "%Y%m%d")
        except ValueError:
            logger.error(" %s - неправильная дата", filename)
            continue

        if file_date > latest_date:
            latest_date = file_date
            latest_file = filepath
            latest_date_str = match.group(1)

    return latest_file, latest_date_str


# Открывает файл и в сжатом объеме
def open_file(filepath: str) -> IO[str]:
    if filepath.endswith(".gz"):
        return gzip.open(filepath, "rt", encoding="utf-8")
    else:
        return open(filepath, "r", encoding="utf-8")


# Парсер строк файла логов
def parse_log_line(line: str) -> dict[str, str | Any] | None:
    line = line.strip()
    if not line:
        logger.info("Строка пустая")
        return None

    match = NGINX_LOG_PATTERN.match(line)
    if not match:
        logger.info("Строка не соответсвует шаблону: %s", line)
        return None

    data = match.groupdict()
    dataReport = {}
    request = data["request"].split()
    if len(request) >= 2:
        dataReport["url"] = request[1]
    else:
        dataReport["url"] = data["request"]

    dataReport["request_time"] = float(data["request_time"])

    return dataReport


# Парсер данных файла
def parse_log_file(filepath: str) -> list[dict]:
    response = []
    with open_file(filepath) as f:
        logger.debug("Файл открыт %s", filepath)
        for line in f:
            data = parse_log_line(line)
            if data is not None:
                response.append(data)

    logger.info("Строки распарсены")
    stats = statisticsFile.get_statistics(response)
    return stats
