from gevent import monkey; monkey.patch_all()  # noqa
from raven import Client

from .worker import Worker


client = Client('http://d64c713263754bef820be968ef3f316f:'
                '0f6cbbd788ba47c7a72f73fb141a81b0'
                '@10.4.232.225:8080/4')

__all__ = [Worker]
