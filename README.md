# ipc-utils
Cross-platform utils for IPC (inter-processing communication) in Python

You can create a named IPC tool like semaphore or mutex here. Onced you created here, you can use it everywhere in your computer. You can also just open a named IPC tool and use it if it has been created somewhere else before.
## Usage
### Semaphore
A named semaphore is offered.
```python
from ipc_utils import Semaphore

sem = Semaphore("/test_sem", create = True, init_val = 1)
## or if it has been created somewhere else before
# sem = Semaphore("/test_sem", create = False)
with sem.guard():
    ... # critical section
## or if you don't want to use "with" syntax
# sem.wait()
# try:
#     ... # critical section
# finally:
#     sem.post()

sem.close()
sem.unlink() # if you want to delete the semaphore. 
             # Don't do this if you are using it somewhere else.
```
Once you created a named semaphore, you can use it in c/cpp like
```c
#ifdef _WIN32
#define Semaphore HANDLE
Semaphore sem = OpenSemaphore(SEMAPHORE_ALL_ACCESS, FALSE, "/test_sem");
#else
#include <semaphore.h>
#define Semaphore sem_t
Semaphore sem = sem_open("/test_sem", 0);
#endif
```
### Mutex
A named mutex is offered.

Note that as posix does not offer named mutex, we use named semaphore with init_val 1 instead.
```python
from ipc_utils import Mutex

mtx = Mutex("/test_mtx", create = True)
## or if it has been created somewhere else before
# mtx = Mutex("/test_mtx", create = False)
with mtx.guard():
    ... # critical section
## or if you don't want to use "with" syntax
# mtx.acquire()
# try:
#     ... # critical section
# finally:
#     mtx.release()

mtx.close()
mtx.unlink() # if you want to delete the mutex. 
             # Don't do this if you are using it somewhere else.
```