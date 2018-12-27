#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/29 14:45
# @Author  : Ryu
# @Site    : 
# @File    : download_file.py
# @Software: PyCharm
import os
import requests
from urllib import parse

def download(courtInfo, item_url):
    url = 'http://wenshu.court.gov.cn/Content/GetHtml2Word'
    headers = {
        'Host': 'wenshu.court.gov.cn',
        'Origin': 'http://wenshu.court.gov.cn',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    fp = open(r'Wenshu_spider\utlis\content.html', 'r', encoding='utf-8')
    htmlName = courtInfo[0]
    htmlStr = fp.readlines()
    fp.close()
    demo = list()
    for i in htmlStr:
        htmlStr = i.replace('court_title', courtInfo[0]).replace('court_date', courtInfo[1]). \
            replace('read_count', courtInfo[2]).replace('court_content', courtInfo[3])
        demo.append(htmlStr)
    htmlStr = ''.join(demo)
    data = {
        'htmlStr': parse.quote(htmlStr),
        'htmlName': parse.quote(courtInfo[0]),
        'DocID': item_url,
    }
    req = requests.post(url, headers=headers, data=data)
    try:
        cont = req.content.decode('utf-8')
    except:
        cont = req.text
    if ('服务不可用' in cont) or ('502' in cont):
        download(courtInfo, item_url)
    else:
        filename = '{}.doc'.format(htmlName)
        fp = open('{}.doc'.format(htmlName), 'wb')
        fp.write(req.content)
        fp.close()

def with_shh(name, content, id):
    with open(name, 'wb') as f:
        f.write(content)
