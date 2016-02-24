#!/usr/bin/env python
#! coding: utf-8

import multiprocessing
import time

pool = None

def my_work(args):
    print args
    return args


def thread():
    while True:
        r = pool.apply(my_work, ("nihao", ))
        print r
        time.sleep(1)

if __name__ == "__main__":
    pool = multiprocessing.Pool()
    thread()
