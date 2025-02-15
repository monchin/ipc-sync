from __future__ import annotations

import ctypes
import multiprocessing as mp
from multiprocessing.sharedctypes import RawArray
from typing import Literal, MutableSequence

import pytest

from ipc_utils import SYS, Mutex, Semaphore

if SYS == "Windows":
    import pywintypes

    PlatFormError = pywintypes.error


def test_create():
    with pytest.raises(PlatFormError):
        Semaphore("/test_sem", False)

    sem = Semaphore("/test_sem", True)
    sem.close()
    sem.unlink()

    with pytest.raises(PlatFormError):
        Semaphore("/test_mtx", False)

    mtx = Mutex("/test_mtx", True)
    mtx.close()
    mtx.unlink()


def kernel(int_buf: MutableSequence[int], mode: Literal["mutex", "semaphore"]):
    obj_name = f"/test_{mode}"
    if mode == "mutex":
        obj = Mutex(obj_name, True)
    elif mode == "semaphore":
        obj = Semaphore(obj_name, False)
    for _ in range(10000):
        with obj.guard():
            int_buf[0] += 1
    obj.close()


def body_for_test(mode: Literal["mutex", "semaphore"]):
    obj_name = f"/test_{mode}"
    if mode == "mutex":
        obj = Mutex(obj_name, True)
    elif mode == "semaphore":
        obj = Semaphore(obj_name, True, 1)
    buf = RawArray(ctypes.c_int, 1)
    for _ in range(5):
        buf[0] = 0
        p1 = mp.Process(target=kernel, args=(buf, mode))
        p2 = mp.Process(target=kernel, args=(buf, mode))
        p1.start()
        p2.start()
        p1.join()
        p2.join()
        assert buf[0] == 20000
    obj.close()
    obj.unlink()


def test_semaphore_guard():
    body_for_test("semaphore")


def test_mutex_guard():
    body_for_test("mutex")
