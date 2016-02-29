#!/usr/bin/env python
#! coding: utf-8

from collections import deque
import gevent
import commands


g_queue = deque([])
seq = 0
judge = "((${value} < 20))"


def get_values():
    import time
    print "get_values()", time.time()
    global seq
    for i in range(500):
        g_queue.append(seq + i)
    seq += 500
    gevent.sleep(1)


def calc_values():
    print "calc_values()"
    global g_queue
    i = g_queue.popleft()
    try:
        while i is not None:
            cmd = "bash -c 'export value=%s;%s'" % (i, judge)
            #print cmd
            status, output = commands.getstatusoutput(cmd)
            #print "i=%d, status=%s" % (i, status)
            i = g_queue.popleft()
    except IndexError:
        gevent.sleep(0)


if __name__ == "__main__":
    while True:
        gevent.joinall([gevent.spawn(get_values), gevent.spawn(calc_values)])
