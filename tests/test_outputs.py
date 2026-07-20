import json
import re
from collections import Counter
from pathlib import Path

REPORT_PATH = Path("/app/report.json")
LOG_PATH = Path("/app/access.log")

REQUEST_LINE_RE = re.compile(r'"[A-Z]+\s+(\S+)\s+HTTP/\d\.\d"')


def _expected_stats() -> dict:
    """Ground truth, independently re-derived from /app/access.log."""
    lines = [line for line in LOG_PATH.read_text().splitlines() if line.strip()]
    ips = {line.split()[0] for line in lines}
    paths: Counter = Counter()
    for line in lines:
        match = REQUEST_LINE_RE.search(line)
        if match:
            paths[match.group(1)] += 1
    return {
        "total_requests": len(lines),
        "unique_ips": len(ips),
        "top_path": paths.most_common(1)[0][0],
    }


def _load_report() -> dict:
    return json.loads(REPORT_PATH.read_text())


def test_report_is_valid_json():
    """Success criterion 1: /app/report.json exists and contains a valid JSON object."""
    assert REPORT_PATH.exists(), "no report.json found at /app/report.json"
    report = _load_report()
    assert isinstance(report, dict), "report.json must contain a single JSON object"


def test_total_requests_matches_log():
    """Success criterion 2: total_requests equals the number of log lines."""
    expected = _expected_stats()
    report = _load_report()
    assert report.get("total_requests") == expected["total_requests"]


def test_unique_ips_matches_log():
    """Success criterion 3: unique_ips equals the number of distinct client IPs."""
    expected = _expected_stats()
    report = _load_report()
    assert report.get("unique_ips") == expected["unique_ips"]


def test_top_path_matches_log():
    """Success criterion 4: top_path equals the single most frequently requested path."""
    expected = _expected_stats()
    report = _load_report()
    assert report.get("top_path") == expected["top_path"]
