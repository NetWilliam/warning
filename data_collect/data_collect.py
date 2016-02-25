#!/usr/bin/env python
#! coding: utf-8

import os
import pyinotify
from public import message # noqa
from stump import monitor_conf # noqa

path_to_name = {}
name_to_path = {}
is_dir = {}
wdds = {}
fw = None


class FileEventHandler(pyinotify.ProcessEvent):
    def __init__(self):
        super(FileEventHandler, self).__init__()

    def process_IN_MODIFY(self, event):
        if event.pathname not in is_dir or not is_dir[event.pathname]:
            # if you listen on a, then you `mv a b`, then you `echo "something" >> b`
            # you'll get an modify event on b
            # that's not what i want when nginx auto-split and rename the log file
            return
        print "MODIFY event:", event

    def process_IN_CREATE(self, event):
        print "CREATE event:", event
        pathname = event.pathname
        if not is_dir[pathname]:
            # FIXME 老的 watcher 没有被删除
            fw.add_file_to_watch(path_to_name[pathname], pathname)

    def process_IN_MOVE_TO(self, event):
        print "MOVE to event:", event
        import pprint
        pprint.pprint(event)


class FileWatcher(object):
    mask = pyinotify.IN_CREATE | pyinotify.IN_MODIFY

    def __init__(self, watch_tuple):
        self._wm = pyinotify.WatchManager()
        for name, path in watch_tuple:
            self.add_file_to_watch(name, path)
        self._eh = FileEventHandler()

    def add_file_to_watch(self, watch_name, file_path):
        file_path = os.path.abspath(file_path)
        file_dir_path = os.path.dirname(file_path)
        wdd = self._wm.add_watch(file_path, FileWatcher.mask, rec=False)
        wdds.update(wdd)
        is_dir[file_path] = False
        wdd = self._wm.add_watch(file_dir_path, FileWatcher.mask, rec=False)
        wdds.update(wdd)
        is_dir[file_dir_path] = True

        path_to_name[file_dir_path] = watch_name
        path_to_name[file_path] = watch_name
        name_to_path[watch_name] = file_path

    def remove_file_from_watch(self, wdd):
        self._wm.rm_watch(wdd)

    def start_monitor(self):
        notifier = pyinotify.Notifier(self._wm, self._eh)
        # forever loop and never return
        notifier.loop()

if __name__ == "__main__":
    fw = FileWatcher([('afile', './a')])
    fw.start_monitor()
