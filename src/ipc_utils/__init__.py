__version__ = "0.0.1"

from ._env import SYS

if SYS == "Windows":
    from ._win import AccessRight, Mutex, Semaphore
else:
    raise NotImplementedError("Only Windows is supported")

__all__ = ["Mutex", "Semaphore"]

if SYS == "Windows":
    __all__ += ["AccessRight"]
