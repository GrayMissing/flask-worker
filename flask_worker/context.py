# coding=utf-8


class Context(object):

    def __init__(self):
        self.tasks = {}

    def clear(self):
        self.tasks.clear()


context = Context()
