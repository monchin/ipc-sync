__version__ = "0.0.1"

from ._env import SYS

if SYS == "nt":
    from ._win import AccessRight, Mutex, Semaphore
elif SYS == "posix":
    from ._posix import Mutex, Semaphore

__all__ = ["Mutex", "Semaphore"]

if SYS == "nt":
    __all__ += ["AccessRight"]
