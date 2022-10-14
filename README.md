# yarl

`yarl` (Yet Another Rate Limiter) is a Python package for rate limiting function
calls.

A lot of Python rate limiting packages seem to exist, but many of them do not
have the desired behavior in many use cases. For example, many clear tasks only
when the period has elapsed, rather than using a sliding window, or they may
mark a task as done prior to running the function rather than after.

`yarl` uses a sliding window of completion times to enforce the rate limit, and
is simple to use. `yarl` currently supports single and multithreaded execution.

## Table of Contents

- [Quickstart](#quickstart)
- [Having multiple functions limited
  together](#having-multiple-functions-limited-together)

## Quickstart

For example, the default Google Docs read request quota might be 300 requests
per minute:

```python3
from yarl import rated_limited

@rate_limited(max_calls=300, period_s=60)
def make_read_request(file_id):
    ...  # some request to the Google Docs API


for file_id in file_ids:
    res = make_read_request(file_id)
```

## Having multiple functions limited together

Sometimes, you want to limit multiple functions together such that their calls
count towards the same rate.

```python3
from yarl import RateLimiter

rate_limiter = RateLimiter(max_calls=300, period_s=60)

@rate_limiter
def make_read_request_one(file_id) -> bool:
    ...  # some request to the Google Docs API


@rate_limiter
def make_read_request_two(file_id):
    ...  # some other request to the Google Docs API


for file_id in file_ids:
    if make_read_request_one(file_id):
        make_read_request_two(file_id)
```
