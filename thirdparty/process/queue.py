# -*- coding: utf-8 -*-
__author__ = 'wangjian'
__time__ = '2020-05-29'
from multiprocessing import Queue
import json

'''
用于存储上游任务的消息, 唯一关键字, task_id
类似于golang 的channel
保留拓展分布式,
如果 不想使用queue，可以考虑用redis zset 来实现，但需要注意分布式中的数据读写一致问题
'''


class TaskQueue(object):
    def __init__(self, save_key: str = 'default_task'):
        self.save_key = save_key
        self.queue = Queue()

    def load_queue(self):
        '''
        load redis task to queue
        :return:
        '''
        pass

    def pop_task(self):
        '''
        get task from queue
        :return:
        '''
        if self.queue_size() == 0:
            return None
        try:
            return self.queue.get()
        except:
            return None

    def put_task(self, obj):
        '''
        put task to
        :param obj:
        :return:
        '''
        try:
            task_id = self.raise_task_id()
            data = json.dumps({
                'task_id': task_id,
                'task_obj': obj
            })
            self.queue.put(data)
            return task_id
        except:
            return

    @staticmethod
    def raise_task_id():
        '''
        from redis incrby: 'task_id'
        :return:
        '''
        pass
        return 0

    def queue_size(self):
        '''
        queue size
        :return:
        '''
        return self.queue.qsize()

    '''
    落地存储, 存储到redis 中(zset)
    '''

    def save_queue(self):
        '''
        save queue to redis
        :return:
        '''
        pass


class ResultQueue(object):
    '''
    投放result,到结果中, 同步结果到redis中, 这里的同步，不再这里操作，而是业务层来做
    '''

    def __init__(self, save_key: str = 'default_result'):
        self.save_key = save_key
        self.queue = Queue()

    def put_result(self, task_id, obj):
        if not task_id or not obj:
            return None
        try:
            data = json.dumps({
                'task_id': task_id,
                'task_obj': obj
            })
            return self.queue.put(data)
        except:
            return None

    def get_task(self):
        try:
            return self.queue.get()
        except:
            return None

    def queue_size(self):
        '''
        get queue size
        :return:
        '''
        return self.queue.qsize()

    def all_result(self):
        '''
        get all result. Reserved func
        :return:
        '''
        pass

    def save_result(self):
        '''
        save result to redis. key => self.save_key
        :return:
        '''
