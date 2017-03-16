# coding=utf-8
import json

from .context import context


class Message(object):

    def __init__(self, task, args, kwargs):
        self.task = task
        self.args = args
        self.kwargs = kwargs

    def ack(self):
        self.task.start(*self.args, **self.kwargs)

    def __str__(self):
        return str({
            "task": self.task,
            "args": self.args,
            "kwargs": self.kwargs
        })

    def dumps(self):
        return json.dumps((self.task.__name__, self.args, self.kwargs))

    @classmethod
    def loads(cls, pkl):
        task_name, args, kwargs = json.loads(pkl)
        task = context.tasks[task_name]
        return cls(task, args, kwargs)
