from __future__ import annotations

from typing import Final

import win32api
import win32event

from ._base import BaseSemaphore

__all__ = ["Semaphore", "AccessRight"]


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
                self._sem = win32event.CreateSemaphore(None, init_val, init_val, name)
            else:
                self._sem = win32event.OpenSemaphore(mode, False, name)

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
