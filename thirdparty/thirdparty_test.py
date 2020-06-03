# -*- coding: utf-8 -*-
__author__ = 'wangjian'
__time__ = '2020-06-03'

from thirdparty.kafka.kafka_cluster import KafkaDao
from thirdparty.process.adb_process import AdbMaster, AdbWorker
import settings
from thirdparty.process import generate_worker_id
import json
from common import logger

logger.init_logger()

def send_kafka_msg(msg):
    kafka_cluster = KafkaDao()
    kafka_cluster.send_message(settings.Conf.get('kafka_info', 'adb_cmd_event'),msg)


def init_process():
    master = AdbMaster()
    for i in range(settings.PROCESS_WORKER):
        worker_id = generate_worker_id()
        master.add_worker(AdbWorker(worker_id))

    master.start()


msg = {
    'event_type': 'adb',
    'event_time': 1587130681,
    'event_skip': 1,  # 1. can skip, 2. cannot skip
    'event_biz': {
        'adb_cmd': 'screen',
        'adb_file': ''  # save result file, adb pull save or read file
    }
}

send_kafka_msg(json.dumps(msg))
init_process()
