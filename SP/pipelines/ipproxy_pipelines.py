# -*- coding: utf-8 -*-
__author__ = 'wuhai'
import json
import logging

import MySQLdb
import MySQLdb.cursors
import redis
from twisted.enterprise import adbapi

logger = logging.getLogger(__name__)


class MysqlTwistedPipline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_crawler(cls, crawler):
        dbparms = dict(
            host=crawler.settings["MYSQL_HOST"],
            db=crawler.settings["MYSQL_DBNAME"],
            user=crawler.settings["MYSQL_USER"],
            passwd=crawler.settings["MYSQL_PASSWORD"],
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool("MySQLdb", **dbparms)
        return cls(dbpool)

    def process_item(self, item, spider):
        # 使用twisted将mysql插入变成异步执行
        query = self.dbpool.runInteraction(self.insert, item)
        query.addErrback(self.handle_error, item, spider)
        return item

    def handle_error(self, failure, item, spider):
        # 处理异步插入的异常
        logger.error(failure)

    def insert(self, cursor, item):
        cmd = item.get_insert_sql()
        cursor.execute(cmd)


class RedisPipeline(object):

    def open_spider(self, spider):
        host = spider.settings.get("REDIS_HOST", "localhost")
        port = spider.settings.get("REDIS_PORT", 6379)
        db_index = spider.settings.get("REDIS_DATABASE", 0)
        db_pwd = spider.settings.get("REDIS_PASSWORD", "")
        # 连接数据库
        self.conn = redis.StrictRedis(host=host, port=port, db=db_index, password=db_pwd)
        # 爬取数据之前，清空之前的ip_proxy
        self.conn.delete("ip_proxy")

    def process_item(self, item, spider):
        item_dict = dict(item)
        # self.conn.hmset(':'.join(['ip_proxy', item_dict['ip']]), item_dict)
        self.conn.lpush("ip_proxy", json.dumps(item_dict))
        return item

    def close_spider(self, spider):
        self.conn.connection_pool.disconnect()
