# -*- coding: utf-8 -*-
__author__ = 'wangjian'
__time__ = '2020-05-28'
from collections.abc import MutableMapping
import threading, os, socket


class ThreadLocalStorage(MutableMapping):
    def __init__(self):
        self.storage = threading.local()
        self.storage.ctx = {}

    def __setitem__(self, key, value):
        self.store.ctx[key] = value

    def __getitem__(self, item):
        return self.store.ctx.get(item, '')

    def __delitem__(self, key):
        del self.store.ctx[key]

    def __iter__(self):
        return self.store.ctx.__iter__()

    def __len__(self):
        return len(self.store.ctx)


thread_local_ctx = ThreadLocalStorage()


def generate_logid():
    try:
        import datetime
        now = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")

        real_ip = os.environ.get("HOST_IP_ADDR", host_ip())
        real_ip = ''.join([x.zfill(3) for x in real_ip.split('.')])

        import uuid
        rand_num = ("%05d" % (uuid.uuid4().int & (1 << 64) - 1))[:5]
    except:
        return 0

    return '{}{}{}'.format(now[:14], real_ip, now[14:17], rand_num)


def host_ip():
    return socket.gethostbyname(socket.gethostname())
