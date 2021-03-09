# -*- coding: utf-8 -*-
__author__ = 'wuhai'
import re

import scrapy

from SP.items.items import *


class ProxyItem(scrapy.Item):
    ip = scrapy.Field()
    port = scrapy.Field()
    type = scrapy.Field()
    updated_time = scrapy.Field()

    def get_insert_sql(self):
        ip = self.get("ip")
        port = self.get("port")
        # 合法ip和port则入库
        if re.match(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', ip) and port.strip().isdigit():
            insert_sql = "INSERT IGNORE INTO ip_proxy " \
                         "(ip, port, type, updated_time) VALUES ('%s', '%s', '%s', '%s')" \
                         % (ip, port, self.get("type"), self.get("updated_time", "0000-00-00"))
            return insert_sql
