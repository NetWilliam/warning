#!/usr/bin/env python
#! coding: utf-8

import time
from collections import deque
import gevent
import commands
from parser import parser
#from multiprocessing import Pool

g_queue = deque([])
seq = 0
#judge = "((${value} < 20))"
judge = "value<20"
#pool = Pool()


def get_values():
    import time
    print "get_values()", time.time()
    global seq
    for i in range(10000):
        g_queue.append(seq + i)
    seq += 10000
    gevent.sleep(1)


def exec_bash(i):
    cmd = "bash -c 'export values=%s;%s'" % (i, judge)
    status, output = commands.getstatusoutput(cmd)
    return status, output


def calc_values():
    print "calc_values()"

    '''
    pool = Pool()
    pool.map(exec_bash, g_queue)
    pool.close()
    pool.join()
    '''
    global g_queue
    i = g_queue.popleft()
    try:
        while i is not None:
            cmd = "value=%s" % i
            res = parser.parse(cmd)
            cmd = judge
            res = parser.parse(cmd)
            #cmd = "value=%s\n%s" % (i, judge)
            #res = parser.parse(cmd)
            #cmd = "bash -c 'export value=%s;%s'" % (i, judge)
            #print cmd
            #status, output = commands.getstatusoutput(cmd)
            #print "i=%d, status=%s" % (i, res)
            i = g_queue.popleft()
    except IndexError:
        print time.time()
        gevent.sleep(0)

if __name__ == "__main__":
    while True:
        gevent.joinall([gevent.spawn(get_values), gevent.spawn(calc_values)])
        #get_values()
        #calc_values()
