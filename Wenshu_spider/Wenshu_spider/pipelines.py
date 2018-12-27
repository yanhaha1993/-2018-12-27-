# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import time
import requests
import pymysql
from twisted.enterprise import adbapi
import gc


class WenshuSpiderPipeline(object):

    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbparams = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            port=settings['MYSQL_PORT'],
            charset='utf8',  # 编码要加上，否则可能出现中文乱码问题
            cursorclass=pymysql.cursors.DictCursor,
            use_unicode=False,
        )
        dbpool = adbapi.ConnectionPool('pymysql', **dbparams)  # **表示将字典扩展为关键字参数,相当于host=xxx,db=yyy....
        return cls(dbpool)  # 相当于dbpool付给了这个类，self中可以得到

    def process_item(self, item, spider):
        self.dbpool.runInteraction(self._conditional_insert, item)
        return item

    def _conditional_insert(self, tx, item):
        table_name = 'table_name'
        ls = list(item)
        sentence = 'INSERT %s (' % table_name + ','.join(ls) + ') VALUES (' + \
                   ','.join(['NULL' if item[l] is None else '%({})r'.format(l) for l in
                             ls]) + ') on duplicate key update ' + ','.join(
            [l + '=' + 'NULL' if item[l] is None else l + '=' + '%({})r'.format(l) for l in ls])
        try:
            tx.execute(sentence % item)
        except BaseException as e:
            print(e)

    def ver_code(self):
        from Wenshu_spider.utlis.chaojiying import Chaojiying_Client
        time.sleep(2)
        session = requests.session()
        chaojiying = Chaojiying_Client('username', 'password', '96001')
        url = 'http://wenshu.court.gov.cn/waf_verify.htm?captcha='
        yanzheng_url = 'http://wenshu.court.gov.cn/waf_captcha/'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
            'Host': 'wenshu.court.gov.cn'
        }
        r = session.get(yanzheng_url, headers=headers)
        result = chaojiying.PostPic(r.content, 1004)
        print(result)
        result = result['pic_str']
        temp_list = r.headers.get('Set-Cookie').split(';')[:1]
        cookies = {temp.split('=', 1)[0]: temp.split('=', 1)[1] for temp in temp_list}
        session.get(url + result, headers=headers, cookies=cookies)

