#!/usr/bin/env python
#! coding: utf-8

import redis

rc = redis.Redis(host="devdb")

ps = rc.pubsub()

ps.subscribe(["foo", "bar"])

for item in ps.listen():
    import pprint
    pprint.pprint(item)
    if item["type"] == "message":
        print item["data"]
