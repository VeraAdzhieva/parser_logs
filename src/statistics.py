import statistics
from collections import defaultdict
from typing import Any

import structlog

structlog.configure()
logger = structlog.get_logger()


# Группирует данные по url
def group_by_url(data: list) -> dict[Any, Any]:
    groups = defaultdict(list)
    for row in data:
        url = row.get("url")
        time = row.get("request_time")
        if url and time is not None:
            groups[url].append(time)

    return dict(groups)


# Рассчитывает статистику для каждого url
def calculate_url_stats(url_data: list[float], alls: dict) -> dict:
    return {
        "count": len(url_data),
        "count_perc": round((len(url_data) / alls["all_count"]) * 100, 3),
        "time_sum": round(sum(url_data), 3),
        "time_perc": round((sum(url_data) / alls["total_time"]) * 100, 3),
        "time_avg": round(statistics.mean(url_data), 3),
        "time_max": max(url_data),
        "time_med": round(statistics.median(url_data), 3),
    }


# Получает статистические данные по файлу
def get_statistics(data: list) -> list[dict]:
    all_count = len(data)
    total_time = sum(item.get("request_time", 0) for item in data)
    alls = {"all_count": all_count, "total_time": total_time}
    logger.debug("Общее кол-во строк: %s , общее время: %s", all_count, total_time)
    groups = group_by_url(data)
    stats = {}
    for url, url_data in groups.items():
        stats[url] = calculate_url_stats(url_data, alls)

    return [{"url": url, **statistics} for url, statistics in stats.items()]
