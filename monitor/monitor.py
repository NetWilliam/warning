#!/usr/bin/env python
#! coding: utf-8

#import Queue
import threading
import gevent
from gevent import queue
import configure

interval = 0.1 # 0.1 second


class FileWatcher():

    def __init__(self, monitors, monitor_filter_queues):
        self._monitors = monitors
        self._monitor_filter_queues = monitor_filter_queues

    def start_watch_loop(self):
        while True:
            print "passive loop forever"

    def on_event_file_modify(self, event):
        dispatch_file_mod(event.message, self._monitor_filter_queues)


def dispatch_file_mod(task, monitor_filter_queues):
    for i in monitor_filter_queues:
        i.put(task)


class Worker():

    def __init__(self, monitor, monitor_filter_queue):
        self._monitor = monitor
        self._consumer_queue = monitor_filter_queue

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


def set_monitor(monitor_queue):
    monitors = configure.get_monitors()
    monitor_cnt = len(monitors)

    monitor_filter_queues = [queue.Queue() for i in xrange(monitor_cnt)]
    workers = [Worker(monitors[i], monitor_filter_queues[i]) for i in xrange(monitor_cnt)]

    timer = threading.Timer(interval, on_point_one_second_timer, [monitors, monitor_queue])
    timer.start()

    file_watcher = FileWatcher(monitors, monitor_filter_queues)
    jobs = [
        gevent.spawn(file_watcher.start_watch_loop),
    ] + [
        gevent.spwan(worker.work) for worker in workers
    ]
    return jobs
    #gevent.joinall(jobs)


class WarningFilter():

    def __init__(self, warning, warning_filter_queues):
        self._name = warning.name
        self._formula = warning.formula
        self._trigger_cycle = warning.trigger_cycle
        self._continuous_cycle = warning.continuous_cycle
        self._alert = warning.alert
        self._monitor_type = warning.monitor_type
        self._queue = queue.Queue(maxsize=self._continuous_cycle)
        warning_filter_queues[self._monitor_type].append(self._queue)

    def register_message(self):
        while True:
            self._next_message = self._queue.get()
            self.filter_and_warning()

    def send_alert(self):
        pass

    def filter_and_warning(self):
        some_condition = self.some_work(self._next_message)
        if some_condition:
            self.send_alert()


def on_monitor_message_received(monitor_queue, warning_filter_queues):
    while True:
        new_monitor_messages = monitor_queue.get()
        dispatch_warning(new_monitor_messages, warning_filter_queues)


def dispatch_warning(monitor_messages, warning_filter_queues):
    for i in xrange(len(warning_filter_queues)):
        monitor_message = monitor_messages[i]
        for message_queue in warning_filter_queues:
            message_queue.put[monitor_message]


def set_warning_filter(monitor_queue):
    warnings = configure.get_warnings()
    warning_cnt = len(warnings)
    print warning_cnt
    warning_filter_queues = [[] for i in xrange(configure.monitor_type_kinds)] # noqa
    if len(warning_filter_queues) != len(monitor_queue):
        pass # error handle
    filters = [WarningFilter(warning) for warning in warnings]
    jobs = [
        gevent.spawn(on_monitor_message_received, monitor_queue, warning_filter_queues)
    ] + [
        gevent.spawn(filter.register_message) for filter in filters
    ]
    return jobs


if __name__ == "__main__":
    monitor_queue = queue.Queue()
    monitor_jobs = set_monitor(monitor_queue)
    warning_jobs = set_warning_filter(monitor_queue)
    gevent.joinall(monitor_jobs + warning_jobs)
