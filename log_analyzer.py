import argparse
import json
import os

import structlog

import src.parser_file as parserFile
import src.report as report
import src.syslog as syslog

config = {
    "REPORT_SIZE": 10,
    "REPORT_DIR": "./reports",
    "LOG_DIR": "./log",
    "TEMPLATE_FILENAME": "nginx-access-ui.log-",
    "SYSLOG_FILE": "./syslog/syslog.log",
}

structlog.configure()
logger = structlog.get_logger()


# Получает значения конфига (в приоритете данные из файла)
def load_config(config_path: str) -> dict:
    if not os.path.exists(config_path):
        raise Exception("Файл не найден")

    try:
        with open(config_path, "r") as f:
            try:
                file_config = json.load(f)
            except json.JSONDecodeError:
                file_config = {}
    except Exception:
        raise Exception("Не удалось прочитать конфиг")

    final_config = {**config, **file_config}
    return final_config


def main(config: dict) -> None:
    try:
        syslog_file = config.get("SYSLOG_FILE")
        syslog.setup_logging(syslog_file)
        log_file, log_date = parserFile.get_last_logfile(config)
        logger.info("Данные файла получены %s", log_file)
        stats = parserFile.parse_log_file(log_file)
        logger.info("Статистичка получена")
        report.generate_report(config, stats, log_date)
        logger.info("Отчет сгенерирован по файлу %s", log_file)

    except Exception as e:
        logger.error("Unexpected error occurred", error=str(e), exc_info=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Log Analyzer")
    parser.add_argument("--config", type=str, default="./config.json")
    args = parser.parse_args()

    config = load_config(args.config)

    main(config)
