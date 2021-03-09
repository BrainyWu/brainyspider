# -*- coding: utf-8 -*-
__author__ = 'wuhai'
import logging

import MySQLdb
import MySQLdb.cursors
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
