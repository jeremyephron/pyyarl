"""
File: rate_limiter.py
---------------------
Defines the RateLimiter decorator class for limiting the rate at which
some callable can be called.

"""

import functools
import threading
import time
from queue import deque

from typing import Any, Callable


class RateLimiter:
    """
    Rate limits decorated callables.

    Can apply a single, shared rate limit to multiple callables.

    Attrs:
        max_calls: The maximum number of calls that can be made per period.
        period_ns: The period in ns during which max_calls calls can be made.
        n_tasks_in_progress: The number of tasks that have been queued but not
            finished executing.
        total_n_completed_tasks: The total number of tasks that have completed
            execution.

        _lock: A lock over in progress and completed tasks.
        _completed_tasks: The deque of completed task times in ns.

    """

    def __init__(self, max_calls: int, period_s: float) -> None:
        self.max_calls = max_calls
        self.period_ns = int(period_s * 1e9)

        self.n_tasks_in_progress = 0
        self.total_n_completed_tasks = 0

        self._lock = threading.Lock()
        self._completed_tasks = deque(maxlen=self.max_calls)

    def __call__(self, func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            with self._lock:
                while (
                    self.n_tasks_in_progress + len(self._completed_tasks)
                    >= self.max_calls
                ):
                    time_until_expiry_ns = (
                        time.monotonic_ns() - self._completed_tasks[0]
                    )

                    if time_until_expiry_ns > self.period_ns:
                        self._completed_tasks.popleft()
                    else:
                        time.sleep(time_until_expiry_ns / 1e9)

                self.n_tasks_in_progress += 1

            ret = func(*args, **kwargs)

            with self._lock:
                self._completed_tasks.append(time.monotonic_ns())
                self.n_tasks_in_progress -= 1
                self.total_n_completed_tasks += 1

            return ret

        return wrapper
