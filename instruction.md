There is an Apache-style access log at /app/access.log. Parse it and write a
JSON summary report to /app/report.json.

The report must be a single JSON object with exactly these three keys:

- total_requests: integer, the total number of log lines.
- unique_ips: integer, the number of distinct client IP addresses (the first
  whitespace-separated field of each line).
- top_path: string, the request path (e.g. "/index.html") that appears most
  often across all requests, taken from the quoted request field
  (e.g. "GET /index.html HTTP/1.1").

Your solution is correct when all of the following hold:

1. /app/report.json exists and contains a single valid JSON object.
2. total_requests equals the number of log lines in /app/access.log.
3. unique_ips equals the number of distinct client IP addresses across those
   lines.
4. top_path equals the single most frequently requested path across those
   lines.
