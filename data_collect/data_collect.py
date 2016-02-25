#!/usr/bin/env python
#! coding: utf-8

import pyinotify
from public import message # noqa


class FileEventHandler(pyinotify.ProcessEvent):
    def __init__(self):
        super(FileEventHandler, self).__init__()

    def process_IN_MODIFY(self, event):
        pass

    def process_IN_CREATE(self, event):
        pass


class FileWatcher(object):
    pass
