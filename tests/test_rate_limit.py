"""
File: test_rate_limit.py
------------------------
Basic tests that the package rate limits as intended.

"""

from collections import deque
import time
from typing import Callable

import pytest

import pyyarl


def generate_func(max_calls: int, period_s: float) -> Callable[[], None]:
    times = deque()

    def func() -> None:
        now = time.monotonic()
        times.append(now)

        time.sleep(1e-4)

        while now - times[0] >= period_s:
            times.popleft()

        assert len(times) <= max_calls

    return func


@pytest.mark.parametrize(
    ('max_calls', 'period_s', 'n_calls'),
    [
        (10, 10, 20),
        (50, 1, 1000),
        (10, 0.5, 100),
        (7, 3, 15)
    ]
)
def test_basic_rate_limit(
    max_calls: int,
    period_s: float,
    n_calls: int
) -> None:
    rate_limiter = pyyarl.rate_limited(max_calls=max_calls, period_s=period_s)

    func = rate_limiter(generate_func(max_calls, period_s))

    for _ in range(n_calls):
        func()
