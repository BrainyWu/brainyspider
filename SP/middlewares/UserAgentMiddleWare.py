#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2019/3/28 14:42
# @Author : way
# @Site : 通用
# @Describe: 设置随机请求头的中间件

from fake_useragent import UserAgent


class UserAgentMiddleWare(object):
    def __init__(self, crawler):
        super(UserAgentMiddleWare, self).__init__()
        self.ua = UserAgent()
        self.ua_type = crawler.settings.get("RANDOM_UA_TYPE", "chrome")

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    # 随机获取一个UA
    def get_ua(self):
        return getattr(self.ua, self.ua_type)

    def process_request(self, request, spider):
        request.headers.setdefault('User-Agent', self.get_ua())
