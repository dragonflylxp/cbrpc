# coding: utf-8

import redis
import memcache
from pymongo import *

from util.connection import PoolManager

configs = {}

def set_up(confs):
    """设置默认（连接）参数
    """
    configs.update(confs)

# 注册自动更新配置
try:
    from configer import JsonConfiger
    JsonConfiger.get_instance().register_auto_updater(set_up, 'database')
    JsonConfiger.get_instance().register_auto_updater(PoolManager.set_up, 'database/mysql')
except Exception as ex:
    pass


########################################


redis_pools = {}
mongodb_pools = {}


def get_redis(dbid, standalone=False):
    conf = configs['redis'][dbid].copy()
    if standalone:
        conf.pop('max_connections', None)
        return redis.Redis(**conf)
    pool = redis_pools.get(dbid)
    if not pool:
        conf.setdefault('max_connections', 8)
        pool = redis.ConnectionPool(**conf)
        redis_pools[dbid] = pool
    return redis.Redis(connection_pool=pool)


########################################


def get_mysql(dbid, standalone=False):
    return PoolManager.instance().get_a_pool(dbid).get_conn()


########################################


class MemCache(object):

    def __init__(self, *args, **kwargs):
        self._client = memcache.Client(*args, **kwargs)

    def __del__(self):
        self.close()

    def __getattr__(self, name):
        return getattr(self._client, name)

    def close(self):
        self._client.disconnect_all()


def get_memcache(dbid):
    # todo: memcache使用连接池
    return MemCache(**configs['memcache'][dbid])

# mongodb
def get_mongo(dbid):
    client_pool = mongodb_pools.get(dbid) 
    if not client_pool:
        client_pool = MongoClient(**configs['mongodb'][dbid])
        mongodb_pools[dbid] = client_pool
    return client_pool 
