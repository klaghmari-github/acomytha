"""Limitation locale des actions sensibles, sans conserver de donnée personnelle brute."""

from __future__ import annotations

from collections import defaultdict, deque
from dataclasses import dataclass
from threading import Lock
from time import monotonic


@dataclass(frozen=True)
class RateLimitResult:
    allowed: bool
    retry_after: int = 0


class RateLimiter:
    """Fenêtre glissante en mémoire, adaptée au déploiement web mono-processus actuel."""

    def __init__(self, enabled: bool = True) -> None:
        self._enabled = bool(enabled)
        self._events: dict[str, deque[float]] = defaultdict(deque)
        self._lock = Lock()

    @property
    def enabled(self) -> bool:
        return self._enabled

    def check(self, key: str, limit: int, window_seconds: int) -> RateLimitResult:
        if not self.enabled:
            return RateLimitResult(True)
        now = monotonic()
        cutoff = now - max(1, window_seconds)
        with self._lock:
            events = self._events[key]
            while events and events[0] <= cutoff:
                events.popleft()
            if len(events) >= max(1, limit):
                retry_after = max(1, int(window_seconds - (now - events[0])) + 1)
                return RateLimitResult(False, retry_after)
            events.append(now)
            return RateLimitResult(True)

    def reset(self, key: str) -> None:
        with self._lock:
            self._events.pop(key, None)
