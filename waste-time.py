#!/usr/bin/env python

from multiprocessing import cpu_count, Pool
import ray

from datetime import datetime as dt
from time import sleep

from itertools import product

import numpy as np

DIV = """
--------------------------------------------------------------------
"""

def log(message=""):
    now = dt.now().time()
    m = (
        """[{now}] :: {message}"""
        .format(
            now=now,
            message=message
        )
    )
    print(m)
    return m, now


### Time Wasters ###
def waste_t(t):
    sleep(t)
    return t


def fib(n):
    if n in {0, 1}:
        return 1
    return fib(n - 1) + fib(n - 2)


### Apply Functions ###
def linear_apply(func, iterable):
    return list(map(func, iterable))


def async_ordered_apply(func, iterable, n=cpu_count()):
    with Pool(n) as p:
        res = p.map(func, iterable)
    return res


def async_unordered_apply(func, iterable, n=cpu_count()):
    with Pool(n) as p:
        res = list(p.imap_unordered(func, iterable))
    return res


def ray_apply(func, iterable):

    @ray.remote
    def _ray_func(*args):
        return func(*args)

    return ray.get([_ray_func.remote(i) for i in iterable])


def waste_t_experiment(async_func, waster_func, iterable):
    s = dt.now()
    res = async_func(waster_func, ts)
    e = dt.now()
    total = e - s
    return total


if __name__ == "__main__":

    ray.init()

    # ts = np.random.rand(50).tolist()
    ts = np.random.randint(37, size=(150,)).tolist()
    log(ts)

    async_funcs = [
        # linear_apply,
        async_ordered_apply,
        async_unordered_apply,
        ray_apply
    ]

    # waster_funcs = [waste_t, fib]
    # waster_funcs = [waste_t]
    waster_funcs = [fib]

    experiments = product(async_funcs, waster_funcs)

    # log(ts)
    log(sum(ts))
    log(sum(ts) / len(ts))

    print(DIV)

    for fa, fw in experiments:

        log(" ---- %s |> %s ---- " % (fa.__name__, fw.__name__))
        total_t = waste_t_experiment(fa, fw, ts)
        log("total time taken: {}".format(total_t.total_seconds()))


    print(DIV)
    ray.shutdown()
