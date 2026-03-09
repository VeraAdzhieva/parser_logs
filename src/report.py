import json
import os

import structlog

structlog.configure()
logger = structlog.get_logger()


# Генерация отчета
def generate_report(config: dict, data: list[dict], log_date: str) -> None:
    template_path = "./reports/report.html"
    report_name = f"report-{log_date}.html"
    report_dir = config.get("REPORT_DIR")
    if not report_dir:
        raise Exception("REPORT_DIR пустой")

    output_path = os.path.join(report_dir, report_name)
    logger.debug("Путь отчета: %s", output_path)
    report_size = config.get("REPORT_SIZE")

    data.sort(key=lambda x: x["time_sum"], reverse=True)

    data = data[:report_size]

    with open(template_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    json_data = json.dumps(data, indent=2, ensure_ascii=False)
    html_content = html_content.replace("$table_json", json_data)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)
