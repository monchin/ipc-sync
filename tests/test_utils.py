from __future__ import annotations

import ctypes
import multiprocessing as mp
from multiprocessing.sharedctypes import RawArray
from typing import Literal, MutableSequence, Union

import pytest  # type: ignore

from ipc_utils import SYS, Mutex, Semaphore

if SYS == "nt":
    import pywintypes

    PlatFormError = pywintypes.error # type: ignore

elif SYS == "posix":
    PlatFormError = OSError # type: ignore


def test_open_non_existing():
    with pytest.raises(PlatFormError):
        Semaphore("/test_sem", False)

    with pytest.raises(PlatFormError):
        Semaphore("/test_mtx", False)


def kernel(int_buf: MutableSequence[int], mode: Literal["mutex", "semaphore"]):
    obj_name = f"/test_{mode}"
    obj: Union[Semaphore, Mutex]
    if mode == "mutex":
        obj = Mutex(obj_name, False)
    elif mode == "semaphore":
        obj = Semaphore(obj_name, False)
    for _ in range(10000):
        with obj.guard():
            int_buf[0] += 1
    obj.close()


def body_for_test(mode: Literal["mutex", "semaphore"]):
    obj_name = f"/test_{mode}"
    obj: Union[Semaphore, Mutex]
    if mode == "mutex":
        obj = Mutex(obj_name, True)
    elif mode == "semaphore":
        obj = Semaphore(obj_name, True, 1)
    buf = RawArray(ctypes.c_int, 1)
    try:
        for _ in range(5):
            buf[0] = 0
            p1 = mp.Process(target=kernel, args=(buf, mode))
            p2 = mp.Process(target=kernel, args=(buf, mode))
            p1.start()
            p2.start()
            p1.join()
            p2.join()
            assert buf[0] == 20000
    finally:
        obj.close()
        obj.unlink()


def test_semaphore_guard():
    body_for_test("semaphore")


def test_mutex_guard():
    body_for_test("mutex")
