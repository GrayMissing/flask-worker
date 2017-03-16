# coding=utf-8
from gevent.queue import Queue
import redis
import time

from .message import Message


class Channel(object):
    def __init__(self):
        self.data = Queue()

    def select(self, timeout=None):
        if len(self.data):
            return True
        return False

    def push(self, message):
        self.data.put(message)

    def pop(self):
        message = self.data.get()
        return message

    def __len__(self):
        return len(self.data)

    def __str__(self):
        data = []
        while not self.data.empty():
            data.append(self.data.get())
        for task in data:
            self.data.put(task)
        return ",".join([str(task) for task in data])

    def cleanup(self):
        pass


class RedisChannel(Channel):
    def __init__(self, host="localhost", port=6379, name="flask_worker_channel"):
        self.data = redis.Redis(host=host, port=port)
        self.name = name

    def select(self, timeout=None):
        if self.data.llen(self.name):
            return True
        return False

    def push(self, message):
        self.data.rpush(self.name, message.dumps())

    def pop(self):
        return Message.loads(self.data.lpop(self.name))

    def __len__(self):
        return self.data.llen(self.name)

    def __str__(self):
        return "<redis channel with len(%d)>" % len(self)

    def cleanup(self):
        self.data.delete(self.name)