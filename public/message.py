#!/usr/bin/env python
#! coding: utf-8

import zmq
import redis

ZMQ_TYPE = "zmq"
REDIS_TYPE = "redis"


class MessagePublisher(object):
    def __init__(self, type=ZMQ_TYPE, bind_to="tcp://*:5678",
                 host="devdb", port=6379):
        self.type = type
        if type == ZMQ_TYPE:
            self._ctx = zmq.Context()
            self._socket = self._ctx.socket(zmq.PUB)
            self._bind_to = bind_to
            self._socket.bind(self._bind_to)
        elif type == REDIS_TYPE:
            self._host = host
            self._port = port
            self._rc = redis.Redis(host=self._host, port=self._port)
        else:
            raise Exception("unsupported type: [%s]!" % self.type)

    def __del__(self):
        if self.type == ZMQ_TYPE:
            self._socket.close()
        elif self.type == REDIS_TYPE:
            pass
        else:
            pass

    def push(self, topic, msg_body):
        if self.type == ZMQ_TYPE:
            self._socket.send_multipart([topic, msg_body])
        elif self.type == REDIS_TYPE:
            self._rc.publish(topic, msg_body)
        else:
            raise Exception("unsupported type: [%s]!" % self.type)


class MessageSubscriber(object):
    def __init__(self, type=ZMQ_TYPE, connect_to="tcp://127.0.0.1:5678",
                 host="devdb", port=6379):
        self.type = type
        self.callback = self.default_callback
        if type == ZMQ_TYPE:
            self._ctx = zmq.Context()
            self._socket = self._ctx.socket(zmq.SUB)
            self._connect_to = connect_to
            self._socket.connect(self._connect_to)
            self._socket.setsockopt(zmq.SUBSCRIBE, "")
        elif type == REDIS_TYPE:
            self._host = host
            self._port = port
            self._rc = redis.Redis(host=self._host, port=self._port)
            self._sub = self._rc.pubsub()
            self._sub.psubscribe(["*"])
        else:
            raise Exception("unsupported type: [%s]!" % self.type)

    def default_callback(self, topic, msg):
        print "Topic: %s, msg: %s" % (topic, msg)

    def set_callback(self, callback):
        self.callback = callback

    def set_topic(self, topic):
        if self.type == ZMQ_TYPE:
            self._socket.setsockopt(zmq.SUBSCRIBE, topic)
        elif self.type == REDIS_TYPE:
            self._sub.subscribe(topic)
        else:
            raise Exception("unsupported type: [%s]!" % self.type)

    def set_topics(self, topics):
        for topic in topics:
            self.set_topic(topic)

    def start_subscribe(self):
        if self.type == ZMQ_TYPE:
            while True:
                topic, msg = self._socket.recv_multipart()
                self.callback(topic, msg)
        elif self.type == REDIS_TYPE:
            for item in self._sub.listen():
                if item["type"] == "message" or item["type"] == "pmessage":
                    self.callback(item["channel"], item["data"])
        else:
            raise Exception("unsupported type: [%s]!" % self.type)
