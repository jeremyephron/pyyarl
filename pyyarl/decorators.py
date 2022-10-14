"""
File: decorators.py
-------------------
Defines decorators for rate limiting callables.

"""

from typing import Callable, Optional

from pyyarl.rate_limiter import RateLimiter


def rate_limited(
    func: Optional[Callable] = None,
    *,
    max_calls: int,
    period_s: float
) -> Callable:
    """
    Decorator for rate limiting callables.

    Just a convenient wrapper for the RateLimiter decorator class.

    Args:
        func: The callable to rate limit.
        max_calls: Maximum number of calls that can be made per period.
        period_s: Period in seconds during which at most max_calls calls to
            function can be made.

    Returns:
        A decorator which will return a rate-limited function if func is None,
        the decorated function otherwise.

    """

    limiter: Callable = RateLimiter(max_calls=max_calls, period_s=period_s)
    return limiter(func) if func else limiter
