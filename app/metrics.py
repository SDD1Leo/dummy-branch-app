from prometheus_client import Counter, Histogram

# Count of requests by endpoint + method + status
REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status"]
)

# Response latency histogram
REQUEST_LATENCY = Histogram(
    "http_request_latency_seconds",
    "Latency of HTTP requests",
    ["endpoint"]
)

# Error counter
ERROR_COUNT = Counter(
    "http_error_total",
    "Total HTTP errors",
    ["endpoint", "status"]
)
