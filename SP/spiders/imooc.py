#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2021-02-25 15:37
# @Author : way
# @Describe : 
from bs4 import BeautifulSoup

from SP.spiders.SPRedisSpider import SPRedisSpider
from SP.utils.make_jobs import ScheduledRequest, RedisCtrl
from SP.utils.make_key import md5
from SP.utils.make_log import log
from SP.utils.tool import get_file_type


class ImoocSpider(SPRedisSpider):
    name = 'imooc'

    redis_key = f'{name}:start_urls'
    allowed_domains = []
    start_urls = ['http://www.imooc.com/']
    custom_settings = {
        'LOG_LEVEL': "INFO",
        'LOG_FILE': log(name),
        'CONCURRENT_REQUESTS': 5,  # 控制并发数，默认16
        'DOWNLOAD_DELAY': 3,  # 控制下载延迟，默认0
        'DOWNLOADER_MIDDLEWARES': {
            'SP.middlewares.UserAgentMiddleWare.UserAgentMiddleWare': 100,
            # 'SP.middlewares.HeadersMiddleWare.MiddleWare': 101,    # 在meta中增加headers
            # 'SP.middlewares.CookiesMiddleWare.MiddleWare': 102,    # 在meta中增加cookies
            # 'SP.middlewares.PayloadMiddleWare.MiddleWare': 103,    # 在meta中增加payload
            # 'SP.middlewares.ProxyMiddleWare.ProxyMiddleWare': 104,  # 使用代理ip
            # 'SP.middlewares.RequestsMiddleWare.RequestMiddleWare': 105,  # 使用requests
            # 'scrapy_splash.SplashCookiesMiddleware': 723,     # 在meta中增加splash 需要启用3个中间件
            # 'scrapy_splash.SplashMiddleware': 725,          # 在meta中增加splash 需要启用3个中间件
            # 'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,    # 在meta中增加splash 需要启用3个中间件
            # 'SP.middlewares.SizeRetryMiddleware.MiddleWare': 900  # 重试中间件，允许设置 MINSIZE（int），response.body 长度小于该值时，自动触发重试
        },
    }

    def parse(self, response):
        pass

