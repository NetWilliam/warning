#!/usr/bin/env python
#! coding: utf-8

import Queue
import threading
import gevent
from gevent import queue
import configure

interval = 0.1


class FileWatcher():

    def __init__(self, monitors, consumer_queues):
        self._monitors = monitors
        self._consumer_queues = consumer_queues

    def start_watch_loop(self):
        while True:
            print "passive loop forever"

    def on_event_file_modify(self, event):
        dispatcher(event.message, self._consumer_queues)


def dispatcher(task, consumer_queues):
    for i in consumer_queues:
        i.put(task)


class Worker():

    def __init__(self, monitor, consumer_queue):
        self._monitor = monitor
        self._consumer_queue = consumer_queue

    def work(self):
        while True:
            task = self._consumer_queue.get()
            message = self._proc_task(task)
            self._monitor.set_message(message)


def on_point_one_second_timer(monitors, monitor_queue):
    msg = []
    for monitor in monitors:
        msg.append(monitor.get_message())
    monitor_queue.put(msg)
    timer = threading.Timer(interval, on_point_one_second_timer, [monitors])
    timer.start()


def start_monitor(monitor_queue):
    monitors = configure.get_monitors()
    monitor_cnt = len(monitors)

    consumer_queues = [queue.Queue() for i in xrange(monitor_cnt)]
    workers = [Worker(monitors[i], consumer_queues[i]) for i in xrange(monitor_cnt)]

    timer = threading.Timer(interval, on_point_one_second_timer, [monitors, monitor_queue])
    timer.start()

    file_watcher = FileWatcher(monitors, consumer_queues)
    jobs = [
        gevent.spawn(file_watcher.start_watch_loop),
    ] + [
        gevent.spwan(worker.work) for worker in workers
    ]
    return jobs
    #gevent.joinall(jobs)


class WarningFilter():

    def __init__(self, name, formula, trigger_cycle, continuous_cycle, alert):
        self._name = name
        self._formula = formula
        self._trigger_cycle = trigger_cycle
        self._continuous_cycle = continuous_cycle
        self._alert = alert
        self._queue = Queue.Queue(maxsize=self._continuous_cycle)

    def on_message_received(self, data):
        pass


def start_warning_filer(monitor_queue):
    warnings = configure.get_warnings()
    warning_cnt = len(warnings)
    print warning_cnt


if __name__ == "__main__":
    monitor_queue = queue.Queue()
    monitor_jobs = start_monitor(monitor_queue)
    warning_jobs = start_warning_filer(monitor_queue)
    gevent.joinall(monitor_jobs + warning_jobs)
