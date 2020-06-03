# -*- coding: utf-8 -*-
__author__ = 'wangjian'
__time__ = '2020-06-01'
from kafka import KafkaConsumer, KafkaProducer
from settings import Conf
from common.logger import msflogger


class KafkaDao(object):
    def __init__(self):
        host_cnf = Conf.items('kafka_info')
        producer_cnf = Conf.items('kafka_producer')
        consumer_cnf = Conf.items('kafka_consumer')
        self.topics = Conf.items('kafka_topics')
        producer_cnf.update(host_cnf)
        consumer_cnf.update(host_cnf)
        self.producer = KafkaProducer(**producer_cnf)

        self.consumer = KafkaConsumer(**consumer_cnf)

    def send_message(self, topic, msg):
        try:
            f = self.producer.send(topic=topic, value=msg)
            print(f.exception, f.is_done)
            print(f.succeeded())
        except Exception as e:
            msflogger.warning(f'send kafka message topic({topic}) error: {str(e)}')
            return None

    def get_consumer(self, topic):
        self.consumer.subscribe(topics=[topic])
        return self.consumer




if __name__ == '__main__':
    k = KafkaDao()
    k.send_message('myTopic', 'ddxxxxd123'.encode(encoding='utf-8'))