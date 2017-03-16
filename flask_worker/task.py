# coding=utf-8
from .message import Message


class Task(object):

    def __init__(self, func, worker):
        self.func = func
        self.worker = worker

    def start(self, *args, **kwargs):
        self.func(*args, **kwargs)

    def delay(self, *args, **kwargs):
        self.worker.default_chan.push(Message(self, args, kwargs))
        return True
