#!/usr/bin/env python
#! coding: utf-8

import configure


def resolve_param():
    pass


def verify(param):
    return configure.verify(param)


def start(param):
    pass


def stop(param):
    pass


def restart(param):
    pass


def main():
    param = resolve_param()
    if param[0] == "verfiy":
        verify(param)
    elif param[0] == "start":
        start(param)
    elif param[0] == "stop":
        stop(param)
    elif param[0] == "restart":
        restart(param)
    else:
        print "usage: controller.py [verify|start|stop|restart] configure_file"
        exit(1)


if __name__ == "__main__":
    main()
