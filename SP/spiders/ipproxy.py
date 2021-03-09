# -*- coding: utf-8 -*-
__author__ = 'wuhai'
import requests

import scrapy
from scrapy.selector import Selector

from SP.spiders.SPRedisSpider import SPRedisSpider
from SP.items.ipproxy_items import ProxyItem
from SP.items.items import FirstItemLoader
from SP.utils.make_log import log


class ProxySpider(SPRedisSpider):
    name = 'proxy'

    redis_key = f'{name}:start_urls'
    allowed_domains = []
    start_urls = ['https://www.kuaidaili.com/free/inha/']
    custom_settings = {
        'LOG_LEVEL': "INFO",
        'LOG_FILE': log(name),
        'CONCURRENT_REQUESTS': 10,  # 控制并发数，默认16
        'DOWNLOAD_DELAY': 1,  # 控制下载延迟，默认0
        'ITEM_PIPELINES': {
            'SP.pipelines.ipproxy_pipelines.MysqlTwistedPipline': 1,
        },
        'DOWNLOADER_MIDDLEWARES': {
            'SP.middlewares.UserAgentMiddleWare.UserAgentMiddleWare': 10,
        },
    }

    def parse(self, response):
        for i in range(1, 50):
            request_url = "{0}{1}/".format(self.start_urls[0], i)
            yield scrapy.Request(url=request_url, callback=self.parse_detail)

    def parse_detail(self, response):
        all_trs = response.xpath("//*[@id='list']//tr")

        for tr in all_trs[1:]:
            # 生成不同的item异步插入数据库，避免主线程item共享异常
            item_loader = FirstItemLoader(item=ProxyItem(), response=response)
            texts = tr.css("td::text").extract()
            item_loader.add_value("ip", texts[0])
            item_loader.add_value("port", texts[1])
            item_loader.add_value("type", texts[3])
            item_loader.add_value("updated_time", texts[-1])

            item = item_loader.load_item()
            yield item
