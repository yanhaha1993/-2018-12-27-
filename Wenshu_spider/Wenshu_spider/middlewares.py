# -*- coding: utf-8 -*-
import random
from Wenshu_spider.user_agents import agents
import base64


class WenshuSpiderDownloaderMiddleware(object):

    def process_request(self, request, spider):
        agent = random.choice(agents)
        request.headers['User-Agent'] = agent

    def process_response(self, request, response, spider):
        html = response.body.decode()
        if response.status != 200 or 'remind key' in html or 'remind' in html or '请开启JavaScript' in html or '服务不可用' in html:
            new_request = request.copy()
            new_request.dont_filter = True
            return new_request
        else:
            return response

    def process_exception(self, request, exception, spider):
        new_request = request.copy()
        new_request.dont_filter = True
        return new_request

class ABProxyMiddleware(object):
    """ 阿布云ip代理配置 """
    def __init__(self, settings):
        self.proxyServer = "http://http-dyn.abuyun.com:9020"
        proxy_user = "key1"
        proxy_pass = "key2"
        self.proxyAuth = "Basic " + base64.urlsafe_b64encode(
            bytes((proxy_user + ":" + proxy_pass), "ascii")).decode("utf8")

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def process_request(self, request, spider):
        request.meta["proxy"] = self.proxyServer
        request.headers["Proxy-Authorization"] = self.proxyAuth

