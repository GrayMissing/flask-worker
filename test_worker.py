# coding=utf-8
from flask_worker import Worker, GeventWorker


def test_background_worker():
    worker = GeventWorker()

    @worker.task
    def helloworld():
        from time import time
        print("Hello World %f" % time())

    worker.start_background()

    for _ in range(1000):
        helloworld.delay()

    worker.join()
    assert not worker.default_chan


def test_worker():
    worker = GeventWorker()

    @worker.task
    def helloworld():
        from time import time
        print("Hello World %f" % time())

    for _ in range(1000):
        helloworld.delay()

    worker.start(temporary=True)
    assert not worker.default_chan


if __name__ == "__main__":
    test_worker()
    test_background_worker()
