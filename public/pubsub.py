#!/usr/bin/env python
#! coding: utf-8

import zmq
import redis

ZMQ_TYPE = "zmq"
REDIS_TYPE = "redis"


class Pub(object):
    def __init__(self, type=ZMQ_TYPE, bind_to="tcp://*:5678",
                 host="devdb", port=6379):
        self._type = type
        if self._type == ZMQ_TYPE:
            self._ctx = zmq.Context()
            self._socket = self._ctx.socket(zmq.PUB)
            self._bind_to = bind_to
            self._socket.bind(self._bind_to)
        elif type == REDIS_TYPE:
            self._host = host
            self._port = port
            self._rc = redis.Redis(host=self._host, port=self._port)
        else:
            raise Exception("unsupported type: [%s]!" % self._type)

    def pub_message(self, message):
        if self._type == ZMQ_TYPE:
            self._socket.send_multipart(message)
        elif self.type == REDIS_TYPE:
            self._rc.publish(message)
        else:
            raise Exception("unsupported type: [%s]!" % self._type)


class Sub(object):
    def __init__(self, type=ZMQ_TYPE, connect_to="tcp://127.0.0.1:5678",
                 host="devdb", port=6379):
        self._type = type
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
            raise Exception("unsupported type: [%s]!" % self._type)

    def sub_message(self):
        if self._type == ZMQ_TYPE:
            return self._socket.recv()
        elif self._type == REDIS_TYPE:
            while True:
                item = self._sub.listen()
                if item["type"] == "message" or item["type"] == "pmessage":
                    return item["data"]
        else:
            raise Exception("unsupported type: [%s]!" % self._type)


class PubSub(object):
    '''
    1 to n publish-subscribe model implementation
    Notice: !!! No multi-threading supported !!!
    '''
    def __init__(self):
        self._pub = None
        self._sub = []

    def _add_subscriber(self, sub, pub):
        pass

    def _remove_subsriber(self, sub, pub):
        pass

    def get_pub(self):
        if self._pub is None:
            self._pub = Pub()
        return self._pub

    def create_sub(self):
        new_sub = Sub()
        self._sub.append(new_sub)
        self._add_subscriber(new_sub, self._pub)
        return len(self._sub) - 1

    def remove_sub(self, sub):
        pass

    def pub_message(self, message):
        return self._pub.pub_message(message)

    def sub_message(self, sub):
        # wait until there are some messages return
        return self._sub[sub].sub_message()
