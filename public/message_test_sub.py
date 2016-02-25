#!/usr/bin/env python
#! coding: utf-8

from message import MessageSubscriber as MS


if __name__ == "__main__":
    ms = MS("redis")
    ms.start_subscribe()
