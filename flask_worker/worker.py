# coding=utf-8
from .channel import Channel
from gevent.pool import Pool
from gevent import idle, spawn

from .task import Task
from .context import context


class BaseWorker(object):

    def __init__(self, app):
        self.app = app

    def start(self):
        pass

    def task(self, func):
        t = Task(func, self)
        t.__name__ = func.__name__
        if t.__name__ not in context.tasks:
            context.tasks[func.__name__] = t
        else:
            raise Exception("Duplicate task name")
        return t


class Slave(BaseWorker):

    def __init__(self, app, pool, message):
        super(Slave, self).__init__(app)
        self.pool = pool
        self.message = message

    def start(self):
        self.pool.apply_async(self.message.ack)


class Worker(BaseWorker):
    pass


class GeventWorker(BaseWorker):

    def __init__(self, app=None, chan=None, num=None):
        super(GeventWorker, self).__init__(app)
        self.default_chan = Channel() if not chan else chan
        self.chans = [self.default_chan]
        if not num:
            import os
            num = os.cpu_count()
        self.pool = Pool(num)
        context.clear()
        if app and not hasattr(app, 'worker'):
            app.worker = self

    def start(self, temporary=False):
        while True:
            # idle to let slave go
            idle()
            if not self.run() and temporary:
                break

    def start_background(self):
        spawn(self.start)

    def run(self):
        find = False
        for chan in self.chans:
            idle()
            if chan.select():
                message = chan.pop()
                slave = Slave(self.app, self.pool, message)
                slave.start()
                find = True
        return find

    def join(self):
        while self.run():
            idle()




