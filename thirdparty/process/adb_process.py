# -*- coding: utf-8 -*-
__author__ = 'wangjian'
__time__ = '2020-05-29'
from thirdparty.process import BaseMaster, BaseWorker
from thirdparty.adb import adb_device
from .queue import TaskQueue, ResultQueue
import settings
from common.decorator import async_call
from common.logger import msflogger

'''
adb process
master + worker: https://www.cnblogs.com/guguobao/p/9398653.html
'''
task_queue = TaskQueue()
result_queue = ResultQueue()


class AdbMaster(BaseMaster):
    process_name = 'adb process'

    def __init__(self):
        self.workers = []
        super(AdbMaster, self).__init__(self.process_name)

    @async_call
    def data_provider(self):
        '''
        parse kafka msg ,then put data to task_queue
        kafka msg pattern
        msg = {
            'event_type': 'adb',
            'event_time': 1587130681,
            'event_skip': 1, # 1. can skip, 2. cannot skip
            'event_biz': {
                'adb_cmd': 'screen',
                'adb_file': '' # save result file, adb pull save or read file
            }
        }
        :return:
        '''
        from thirdparty.kafka.kafka_cluster import KafkaDao
        kafka_client = KafkaDao()
        topic = settings.Conf.get('kafka_info', 'adb_cmd_event')
        data_stream = kafka_client.get_consumer(topic)
        print(data_stream)
        for msg in data_stream:
            msflogger.info(f'get msg({msg}) from data_stream(kafka)')
            print('get task:', msg.val)
            task_queue.put_task(msg.val)

    @async_call
    def result_save(self):
        while True:
            print('get result: ',result_queue.get_task())
            result_queue.save_result()

    def count_worker(self):
        return len(self.workers)

    def add_worker(self, worker):
        '''
        add worker to master
        :return:
        '''
        self.workers.append(worker)

    def start(self):
        self.data_provider()
        self.result_save()
        for w in self.workers:
            w.join()
            w.wait()

    def stop(self):
        for w in self.workers:
            if w.is_alive():
                w.terminate()
                w.close()

    def restart_worker(self):
        import time
        self.stop()
        time.sleep(2)
        self.start()


class AdbWorker(BaseWorker):
    def __init__(self, worker_id):
        super(AdbWorker, self).__init__(worker_id)

    def run(self):
        '''
        get msg from queue. Then do something
        :return:
        '''

        msg = task_queue.pop_task()
        try:
            import json
            data = json.loads(msg)
            if data['event_type'] == 'adb' and data['event_biz']['adb_cmd'] == 'screen':
                ret = adb_device.get_screen_size(adb_device.get_connect_device())
                result_queue.put(ret)
        except Exception as e:
            msflogger(f'adb worker failed. error:{str(e)}')
