
from functools import wraps
from time import time
from typing import Any

def timeit(f):
    @wraps(f)
    def wrap(*args, **kw) -> Any:
        ts = time()
        result = f(*args, **kw)
        te = time()
        print('func:%r args:[%r, %r] took: %2.4f sec' % \
          (f.__name__, args, kw, te-ts))
        return result
    return wrap