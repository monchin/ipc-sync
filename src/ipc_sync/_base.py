from __future__ import annotations

import contextlib
from typing import Final


class BaseSemaphore:
    def __init__(self, name: str, create: bool, init_val: int):
        self._sem = None
        self._name: Final = name
        if create:
            assert init_val > 0, "Initial value must be greater than 0"

    def wait(self):
        raise NotImplementedError

    def post(self):
        raise NotImplementedError

    def close(self):
        raise NotImplementedError

    def unlink(self):
        pass

    @contextlib.contextmanager
    def guard(self):
        self.wait()
        try:
            yield
        finally:
            self.post()


class BaseMutex:
    def __init__(self, name: str):
        self._mutex = None
        self._name: Final = name

    def acquire(self):
        raise NotImplementedError

    def release(self):
        raise NotImplementedError

    def close(self):
        raise NotImplementedError

    def unlink(self):
        pass

    @contextlib.contextmanager
    def guard(self):
        self.acquire()
        try:
            yield
        finally:
            self.release()
