#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2019/4/8 10:44
# @Author : way
# @Site : all
# @Describe: 基础类, 从redis读取请求数据，构造成scrapy请求
import json

from scrapy_redis.spiders import RedisSpider, bytes_to_str
from scrapy import signals
from scrapy.http import Request, FormRequest
from scrapy_splash import SplashRequest, SplashFormRequest

from SP.utils.make_jobs import ScheduledRequest


class SPRedisSpider(RedisSpider):
    start_urls = []

    def handles_start_urls(self, spider):
        for start_url in self.start_urls:
            self.server.lpush(self.redis_key, start_url)

    def start_requests(self):
        """Returns a batch of start requests from redis."""
        for start_url in self.start_urls:
            self.server.lpush(self.redis_key, start_url)
        return self.next_requests()
