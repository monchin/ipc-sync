from __future__ import annotations

from typing import Final

import win32api
import win32event

from ._base import BaseMutex, BaseSemaphore

__all__ = ["AccessRight", "Semaphore"]


class AccessRight:
    DELETE: Final = 0x00010000
    READ_CONTROL: Final = 0x00020000
    SYNCHRONIZE: Final = 0x00100000
    WRITE_DAC: Final = 0x00040000
    WRITE_OWNER: Final = 0x00080000
    EVENT_ALL_ACCESS: Final = 0x001F0003
    EVENT_MODIFY_STATE: Final = 0x0002
    MUTEX_ALL_ACCESS: Final = 0x001F0001
    MUTEX_MODIFY_STATE: Final = 0x0001
    SEMAPHORE_ALL_ACCESS: Final = 0x001F0003
    SEMAPHORE_MODIFY_STATE: Final = 0x0002
    TIMER_ALL_ACCESS: Final = 0x001F0003
    TIMER_MODIFY_STATE: Final = 0x0002
    TIMER_QUERY_STATE: Final = 0x0001


class Semaphore(BaseSemaphore):
    def __init__(
        self,
        name: str,
        create: bool,
        init_val: int = 1,
        mode: int = AccessRight.SEMAPHORE_ALL_ACCESS,
    ):
        super().__init__(name, create, init_val)

        try:
            if create:
                self._sem = win32event.CreateSemaphore(None, init_val, init_val, name) # type: ignore
            else:
                self._sem = win32event.OpenSemaphore(mode, False, name) # type: ignore

        except Exception as e:
            self._sem = None
            raise e

    def wait(self):
        win32event.WaitForSingleObject(self._sem, win32event.INFINITE)

    def post(self):
        win32event.ReleaseSemaphore(self._sem, 1)

    def close(self):
        if self._sem is not None:
            win32api.CloseHandle(self._sem)


class Mutex(BaseMutex):
    def __init__(
        self, name: str, create: bool, mode: int = AccessRight.MUTEX_ALL_ACCESS
    ):
        super().__init__(name)

        try:
            if create:
                self._mutex = win32event.CreateMutex(None, False, name) # type: ignore
            else:
                self._mutex = win32event.OpenMutex(mode, False, name)  # type: ignore
        except Exception as e:
            self._mutex = None
            raise e

    def acquire(self):
        win32event.WaitForSingleObject(self._mutex, win32event.INFINITE)

    def release(self):
        win32event.ReleaseMutex(self._mutex)

    def close(self):
        if self._mutex is not None:
            win32api.CloseHandle(self._mutex)
