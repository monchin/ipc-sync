import ctypes.util
import os
from ctypes import CDLL, c_char_p, c_int, c_void_p

from ._base import BaseMutex, BaseSemaphore

libc = CDLL(ctypes.util.find_library("c"))

libc.sem_open.restype = c_void_p
libc.sem_open.argtypes = [c_char_p, c_int, c_int, c_int]

libc.sem_wait.argtypes = [c_void_p]
libc.sem_post.argtypes = [c_void_p]

libc.sem_close.argtypes = [c_void_p]
libc.sem_unlink.argtypes = [c_char_p]


class Semaphore(BaseSemaphore):
    def __init__(self, name: str, create: bool, init_val: int = 1, mode: int = 0o644):
        super().__init__(name, create, init_val)

        if create:
            self._sem = libc.sem_open(
                self._name.encode("utf-8"), os.O_CREAT | os.O_EXCL, mode, init_val
            )
        else:
            self._sem = libc.sem_open(
                self._name.encode("utf-8"), os.O_RDWR, mode, init_val
            )

        if self._sem is None:
            raise OSError(
                ctypes.get_errno(),
                f"Failed to {'create' if create else 'open'} named semaphore '{self._name}'",
            )

    def wait(self):
        if libc.sem_wait(self._sem) == -1:
            raise OSError(ctypes.get_errno(), "sem_wait failed")

    def post(self):
        if libc.sem_post(self._sem) == -1:
            raise OSError(ctypes.get_errno(), "sem_post failed")

    def close(self):
        if self._sem:
            if libc.sem_close(self._sem) == -1:
                raise OSError(ctypes.get_errno(), "sem_close failed")
            self._sem = None

    def unlink(self):
        if libc.sem_unlink(self._name.encode("utf-8")) == -1:
            raise OSError(ctypes.get_errno(), "sem_unlink failed")


class Mutex(BaseMutex):
    """
    Posix does not offer named mutex, so we use named semaphore with init_val 1
    instead
    """

    def __init__(self, name: str, create: bool, mode: int = 0o644):
        self._mtx = Semaphore(name, create, 1, mode)

    def acquire(self):
        self._mtx.wait()

    def release(self):
        self._mtx.post()

    def close(self):
        self._mtx.close()

    def unlink(self):
        self._mtx.unlink()
