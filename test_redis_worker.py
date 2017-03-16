# coding=utf-8
from flask_worker.channel import RedisChannel
from flask_worker import Worker


def test_redis_worker():
    chan = RedisChannel(host="10.4.232.225")
    worker = Worker(chan=chan)

    @worker.task
    def helloworld():
        from time import time
        print("Hello World %f" % time())

    for _ in range(1000):
        helloworld.delay()

    try:
        worker.start(temporary=True)
    finally:
        worker.default_chan.cleanup()

    assert not worker.default_chan


if __name__ == "__main__":
    test_redis_worker()