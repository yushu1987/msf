# -*- coding: utf-8 -*-
__author__ = 'wangjian'
__time__ = '2020-05-29'
import abc, uuid
from .queue import TaskQueue, ResultQueue
from multiprocessing import Process

__all__ = ['BaseMaster', 'BaseWorker', 'generate_worker_id']


def generate_worker_id():
    return str(uuid.uuid4().int)[:6]


class BaseMaster(object, metaclass=abc.ABCMeta):

    def __init__(self, process_name=''):
        self.process_name = process_name

    @abc.abstractmethod
    def data_provider(self):
        pass

    '''
    启动进程来work
    '''

    @abc.abstractmethod
    def start(self):
        pass

    '''
    终止master 
    '''

    @abc.abstractmethod
    def stop(self):
        pass

    '''
    重启worker
    '''

    def restart_worker(self):
        pass


class BaseWorker(Process, metaclass=abc.ABCMeta):

    def __init__(self, worker_id=''):
        self.worker_id = worker_id
        self.result = {}
        super(Process, self).__init__(daemon=True)

    @abc.abstractmethod
    def run(self):
        pass
