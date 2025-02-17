__version__ = "0.0.1"

from ._env import SYS

if SYS == "nt": # mypy does not support os.name, but it's better than sys.platform here
    from ._win import AccessRight, Mutex, Semaphore  # type: ignore
elif SYS == "posix":
    from ._posix import Mutex, Semaphore  # type: ignore

__all__ = ["Mutex", "Semaphore"]

if SYS == "nt":
    __all__ += ["AccessRight"]
