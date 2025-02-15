from __future__ import annotations

import ctypes
import multiprocessing as mp
from multiprocessing.sharedctypes import RawArray

import pytest

from ipc_utils import SYS, Semaphore

if SYS == "Windows":
    import pywintypes

    PlatFormError = pywintypes.error


def test_create():
    with pytest.raises(PlatFormError):
        Semaphore("/test_sem", False)

    sem = Semaphore("/test_sem", True)
    sem.close()
    sem.unlink()


def kernel(int_buf: RawArray, sem_name: str):
    sem = Semaphore(sem_name, False)
    for _ in range(10000):
        with sem.guard():
            int_buf[0] += 1


def test_semaphore_guard():
    sem_name = "/test_sem"
    sem = Semaphore(sem_name, True)
    buf = RawArray(ctypes.c_int, 1)
    for _ in range(5):
        buf[0] = 0
        p1 = mp.Process(target=kernel, args=(buf, sem_name))
        p2 = mp.Process(target=kernel, args=(buf, sem_name))
        p1.start()
        p2.start()
        p1.join()
        p2.join()
        assert buf[0] == 20000
    sem.close()
    sem.unlink()
