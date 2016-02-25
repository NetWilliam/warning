#!/usr/bin/env python
#! coding: utf-8

import time
from message import MessagePublisher as MP

if __name__ == "__main__":
    mp = MP("redis")
    while True:
        mp.push("hello", "world")
        time.sleep(1)
