# -*- coding: utf-8 -*-
import time

BOT_NAME = 'Wenshu_spider'
SPIDER_MODULES = ['Wenshu_spider.spiders']
NEWSPIDER_MODULE = 'Wenshu_spider.spiders'
ROBOTSTXT_OBEY = False
LOG_FILE = BOT_NAME + '_' + time.strftime("%Y%m%d", time.localtime()) + '.log'
LOG_LEVEL = 'INFO'
LOG_ENABLED = True
LOG_ENCODING = 'utf-8'
LOG_STDOUT = False
RETRY_ENABLED = True
RETRY_TIMES = 3
DNSCACHE_ENABLED = True

CONCURRENT_REQUESTS_PER_SPIDER = 5
CONCURRENT_REQUESTS_PER_DOMAIN = 100
# CONCURRENT_REQUESTS_PER_IP = 16
DOWNLOADER_MIDDLEWARES = {
   'Wenshu_spider.middlewares.WenshuSpiderDownloaderMiddleware': 300,
   # 'Wenshu_spider.middlewares.ABProxyMiddleware': 1,
}
ITEM_PIPELINES = {
   # 'Wenshu_spider.pipelines.WenshuSpiderPipeline': 100,
}

MYSQL_HOST = '127.0.0.1'
MYSQL_DBNAME = 'hello'
MYSQL_USER = 'root'
MYSQL_PASSWD = 'mysql'
MYSQL_PORT = 3306