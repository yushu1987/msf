# -*- coding: utf-8 -*-
__author__ = 'wangjian'
__time__ = '2020-05-28'

import contextlib
from common.decorator import singleton
from common.exception import MsfException, MsfExceptionEnum
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from common.logger import msflogger


@singleton
class MysqlClient(object):

    def __init__(self, pool_size=20, pool_max_size=50, pool_recycle=300):
        try:
            database_uri = self._build_db_uri()
            self.engine = create_engine(
                database_uri,
                pool_size=pool_size,  # 连接池大小
                max_overflow=pool_max_size,  # 连接池最大的大小
                pool_recycle=pool_recycle,  # 多久时间主动回收连接，见下注释
            )
            self.Session = sessionmaker(bind=self.engine)
        except Exception as e:
            raise MsfException(MsfExceptionEnum.DB_CALL_ERROR)

    @staticmethod
    def _build_db_uri():
        mysql_user = ''
        mysql_pass = ''
        mysql_host = ''
        mysql_port = ''
        mysql_charset = ''
        database_uri = 'mysql+pymysql://%s:%s@%s:%s/%s?charset=%s' % (
            mysql_user, mysql_pass, mysql_host, mysql_port, mysql_charset
        )
        return database_uri

    @contextlib.contextmanager
    def get_session(self):
        session = self.Session()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def get_engine(self):
        return self.engine


db = MysqlClient()
BaseModel = declarative_base()


class BaseDal(object):
    def add(self, cls, add_data):
        try:
            with db.get_session() as session:
                return session.add(cls(**add_data)) > 0
        except Exception as e:
            msflogger.warning(f'add data fail. e:{str(e)}')
            return False

    def update(self, cls, where, update_data, limit=1):
        try:
            with db.get_session() as session:
                return session.query(cls).filter_by(**where).update(**update_data).limit(limit) > 0
        except Exception as e:
            msflogger.warning(f'update data fail. e:{str(e)}')
            return False

    def delete(self, cls, where, limit=1, offset=0):
        try:
            with db.get_session() as session:
                return session.query(cls).filter_by(**where).delete().limit(limit).offset(offset) > 0
        except Exception as e:
            msflogger.warning(f'delete data fail. e:{str(e)}')
            return False

    def select(self, cls, where, one=False, limit=1, offset=0):
        try:
            with db.get_session() as session:
                if one:
                    return session.query(cls).filter_by(**where).limit(limit).offset(offset).first()
                else:
                    return session.query(cls).filter_by(**where).limit(limit).offset(offset).all()
        except Exception as e:
            msflogger.warning(f'select data fail. e:{str(e)}')
            return None
