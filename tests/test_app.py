import src.parser_file as parserFile
import src.statistics as statsFile


def test_parse_log_line_success() -> None:
    """Тест парсинга строк файла."""
    line = (
        '1.138.198.128 -  - [30/Jun/2017:03:28:23 +0300] "GET /api/v2/banner/25187824 HTTP/1.1" 200 1260 '
        '"-" "python-requests/2.8.1" "-" "1498782503-440360380-4707-10488749" "4e9627334" 0.203'
    )

    result = parserFile.parse_log_line(line)

    assert result is not None
    assert result["url"] == "/api/v2/banner/25187824"
    assert result["request_time"] == 0.203


def test_calculate_url_stats() -> None:
    """Тест расчёта статистики."""
    times = [0.1, 0.2, 0.3, 0.4, 0.5]
    alls = {"all_count": 10, "total_time": 10}

    stats = statsFile.calculate_url_stats(times, alls)

    assert stats["count"] == 5
    assert stats["count_perc"] == 50
    assert stats["time_sum"] == 1.5
    assert stats["time_perc"] == 15
    assert stats["time_avg"] == 0.3
    assert stats["time_max"] == 0.5
    assert stats["time_med"] == 0.3
