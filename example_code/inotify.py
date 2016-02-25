#!/usr/bin/env python
#! coding: utf-8

import os
import datetime
import pyinotify
import logging
import crash_on_ipy # noqa

## Instanciate a new WatchManager (will be used to store watches).
#wm = pyinotify.WatchManager()
## Associate this WatchManager with a Notifier (will be used to report and
## process events).
#notifier = pyinotify.Notifier(wm)
## Add a new watch on /tmp for ALL_EVENTS.
#wm.add_watch('/tmp', pyinotify.ALL_EVENTS)
## Loop forever and handle events.
#notifier.loop()
#
#
#
#if __name__ == "__main__":
#    pass


class MyEventHandler(pyinotify.ProcessEvent):
    logging.basicConfig(level=logging.INFO,filename='/var/log/monitor.log')
    #自定义写入那个文件，可以自己修改
    logging.info("Starting monitor...")
    def process_IN_ACCESS(self, event):
        print "ACCESS event:", event.pathname
        logging.info("ACCESS event : %s    %s" % (os.path.join(event.path,event.name),datetime.datetime.now()))
    def process_IN_ATTRIB(self, event):
        print "ATTRIB event:", event.pathname
        logging.info("IN_ATTRIB event : %s    %s" % (os.path.join(event.path,event.name),datetime.datetime.now()))
    def process_IN_CLOSE_NOWRITE(self, event):
        print "CLOSE_NOWRITE event:", event.pathname
        logging.info("CLOSE_NOWRITE event : %s    %s" % (os.path.join(event.path,event.name),datetime.datetime.now()))
    def process_IN_CLOSE_WRITE(self, event):
        print "CLOSE_WRITE event:", event.pathname
        logging.info("CLOSE_WRITE event : %s    %s" % (os.path.join(event.path,event.name),datetime.datetime.now()))
    def process_IN_CREATE(self, event):
        print "CREATE event:", event.pathname
        logging.info("CREATE event : %s    %s" % (os.path.join(event.path,event.name),datetime.datetime.now()))
    def process_IN_DELETE(self, event):
        print "DELETE event:", event.pathname
        logging.info("DELETE event : %s    %s" % (os.path.join(event.path,event.name),datetime.datetime.now()))
    def process_IN_MODIFY(self, event):
        print "MODIFY event:", event.pathname
        logging.info("MODIFY event : %s    %s" % (os.path.join(event.path,event.name),datetime.datetime.now()))
        if event.name == "a":
            for line in a_file.readlines():
                print "a modify:", line
        else:
            for line in b_file.readlines():
                print "b modify:", line
    def process_IN_OPEN(self, event):
        print "OPEN event:", event.pathname
        logging.info("OPEN event : %s    %s" % (os.path.join(event.path,event.name),datetime.datetime.now()))

a_file = open('./a', 'r')
a_file.seek(0,2)
b_file = open('./b', 'r')
b_file.seek(0,2)

def main():
    # watch manager
    wm = pyinotify.WatchManager()
    wm.add_watch('./a', pyinotify.ALL_EVENTS, rec=True)
    wm.add_watch('./b', pyinotify.ALL_EVENTS, rec=True)
    wm.add_watch('.', pyinotify.ALL_EVENTS, rec=True)
    # mv b d 没反应
    # touch b 有 create 信号, 在 create 信号中需要重新 add_watch
    # 如果删掉 b 之后 touch b, 需要重新 add_watch
    # 启动之后老日志不要了, 只监控新增的日志, 打开之后 seek(0, 2), 定位到末尾
    # 如果打开失败则说明此文件不存在, 监控这个文件
    #
    #
    #/tmp是可以自己修改的监控的目录
    # event handler
    eh = MyEventHandler()

    # notifier
    notifier = pyinotify.Notifier(wm, eh)
    notifier.loop()

if __name__ == '__main__':
    main()

