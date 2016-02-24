#!/usr/bin/env python
#! coding: utf-8

import redis

rc = redis.Redis(host="devdb")

#ps = rc.pubsub()

#ps.subscribe(["foo", "bar"])

rc.publish("foo", "hello world")
