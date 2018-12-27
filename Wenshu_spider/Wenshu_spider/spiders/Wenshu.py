# -*- coding: utf-8 -*-
import scrapy, time, json, re, execjs
from Wenshu_spider.items import WenshuSpiderItem

class WenshuSpider(scrapy.Spider):  # RedisSpider
    name = 'wenshu'
    start_urls = ['http://wenshu.court.gov.cn/List/List?sorttype=1']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.guid = 'aaaabbbb-aaaa-aaaabbbb-aaaabbbbcccc'
        with open('Wenshu_spider\spiders\get_vl5x.js', encoding='utf-8') as f:
            jsdata_1 = f.read()
        with open('Wenshu_spider\spiders\get_docid.js', encoding='utf-8') as f:
            jsdata_2 = f.read()
        self.js_1 = execjs.compile(jsdata_1)
        self.js_2 = execjs.compile(jsdata_2)
        self.mold = ['合同', '利息', '利率', '合同约定', '民间借贷', '交通事故', '返还', '强制性规定', '担保',
                     '鉴定', '借款合同', '人身损害赔偿', '误工费', '给付', '违约金', '驳回' '贷款', '清偿', '处分',
                     '保证', '赔偿责任', '违约责任', '交付', '离婚', '交通事故损害赔偿', '传票', '夫妻关系', '买卖合同', '传唤',
                     '婚姻', '债权', '民事责任', '债务人', '精神损害', '缺席判决', '残疾赔偿金', '债权人', '分公司', '追偿', '保险合同',
                     '管辖', '第三人', '租赁', '承诺', '垫付', '票据', '变更', '股份有限公司', '抵押', '赔偿金', '连带责任', '本案争议',
                     '劳动合同', '损害赔偿', '赔偿损失', '租金', '保证合同', '物业管理', '解除合同', '所有权', '建设工程', '滞纳金',
                     '劳动争议' '保险人', '侵权行为', '共同债务', '程序合法', '投资', '出卖人', '财产保险', '保人', '抗辩权', '实际损失',
                     '意思表示真实', '补充协议' '合同履行地', '贷款人', '全面履行'  '代理', '被保险人', '不动产', '赔偿数额', '房屋买卖',
                     '主要责任', '标的物', '保证期间', '不履行', '授权', '法定代表人', '抚养费', '合同解除', '反诉', '担保合同',
                     '第三者责任险', '房屋租赁', '']
        self.year_list = ['2018', '2017', '2016', '2015', '2014', '2013', '2012', '2010', '2011', '2009', '2008', '2007',
                          '2006', '2005', '2004', '2002', '2003', '2001', '2000', '1998', '1996', '1995', '1999', '1992',
                          '1997', '1991', '1993', '1994', '1990', '1985', '1986', '1988']

        with open(r'Wenshu_spider\spiders\topnpl_judge_local.txt', 'r', encoding='utf-8') as f:
            file = f.read()
        self.local = file.split('\n')

    def parse(self, response):
        try:
            vjkl5 = response.headers['Set-Cookie'].decode('utf-8')
            vjkl5 = vjkl5.split(';')[0].split('=')[1]
            url_num = 'http://wenshu.court.gov.cn/ValiCode/GetCode'
            data = {
                'guid': self.guid
            }
            yield scrapy.FormRequest(url_num, formdata=data, meta={'vjkl5': vjkl5}, callback=self.get_count,
                                     dont_filter=True)
        except:
            yield scrapy.Request(WenshuSpider.start_urls, callback=self.parse, dont_filter=True)

    def get_count(self, response):
        number = response.text
        vjkl5 = response.meta['vjkl5']
        vl5x = self.js_1.call('getvl5x', vjkl5)
        url = 'http://wenshu.court.gov.cn/List/ListContent'
        year = 2018
        mold_index = 0
        while True:
            if self.mold[mold_index] != '':
                for local in self.local:
                    for index in range(1, 21):
                        data = {
                            'Param': '案件类型:民事案件,裁判年份:{},关键词:{},基层法院:{}'.format(year, self.mold[mold_index], local),
                            'Index': str(index),
                            'Page': '10',
                            'Order': '法院层级',
                            'Direction': 'asc',
                            'vl5x': vl5x,
                            'number': number,
                            'guid': self.guid
                        }
                        headers = {
                            'Cookie': 'vjkl5=' + response.meta['vjkl5'],  # 在这单独添加cookie,settings中就可以禁用cookie,防止跟踪被ban
                            'Host': 'wenshu.court.gov.cn',
                            'Origin': 'http://wenshu.court.gov.cn',
                        }
                        yield scrapy.FormRequest(url,
                                                 formdata=data,
                                                 headers=headers,
                                                 meta={'from_data': data,
                                                       'headers': headers,
                                                       'vjkl5': response.meta['vjkl5']},
                                                 callback=self.get_docid, dont_filter=True)
                mold_index += 1
            else:
                year -= 1
                mold_index = 0
                if year == 1984:
                    break

    def get_docid(self, response):
        item = WenshuSpiderItem()
        html = response.text
        try:
            result = eval(json.loads(html))
            runeval = result[0]['RunEval']
            content = result[1:]
            for cont in content:
                casewenshuid = cont.get('文书ID', '')
                docid = self.js_2.call('getdocid', runeval, casewenshuid)
                print(docid)
                url = 'http://wenshu.court.gov.cn/CreateContentJS/CreateContentJS.aspx?DocID={}'.format(docid)
                yield scrapy.Request(url, callback=self.get_detail,
                                     meta={'vjkl5': response.meta['vjkl5'],
                                           'meta': item},
                                     dont_filter=True)
        except:
            string = response.text.replace('“', '"').replace('\\', '')
            result = eval(string[1:-1])
            content = result[1:]
            for cont in content:
                docid = cont['文书ID']
                print(docid)
                url = 'http://wenshu.court.gov.cn/CreateContentJS/CreateContentJS.aspx?DocID={}'.format(docid)
                yield scrapy.Request(url, callback=self.get_detail,
                                     meta={'vjkl5': response.meta['vjkl5'],
                                           'meta': item},
                                     dont_filter=True)

    def get_detail(self, response):
        item = WenshuSpiderItem()
        html = response.text.encode(response.encoding).decode('utf-8').replace('\ufffd', '')
        item_url = re.compile(r'"文书ID":"(.*?)",', re.S)
        judge_doc_name = re.compile(r'"案件名称":"(.*?)",', re.S)
        judge_code = re.compile(r'"案号":"(.*?)",', re.S)
        judge_name = re.compile(r'"法院名称":"(.*?)",', re.S)
        show_date = re.compile(r'"上传日期":"\\/Date\((.*?)\)\\/",', re.S)
        case_reason = re.compile(r'{ name: "案由", key: "reason", value: "(.*?)" }', re.S)
        judge_object = re.compile(r'{ name: "当事人", key: "appellor", value: "(.*?)" }', re.S)
        judge_rule = re.compile(r'LegalBase: (.*?)};', re.S)
        doc_head = re.compile(r"<a type='dir' name='DSRXX'></a>(.*?)<a", re.S)
        doc_truth = re.compile(r"<a type='dir' name='SSJL'></a>(.*?)<a", re.S)
        doc_truth1 = re.compile(r"<a type='dir' name='AJJBQK'></a>(.*?)<a", re.S)
        doc_reason = re.compile(r"<a type='dir' name='CPYZ'></a>(.*?)<a", re.S)
        doc_rusult = re.compile(r"<a type='dir' name='PJJG'></a>(.*?)<a", re.S)
        doc_bottom = re.compile(r"<a type='dir' name='WBWB'></a>(.*?)\\\"}\"", re.S)
        judge_prosecution = re.compile(r"机关：(.*?)[。]<", re.S)
        Pub_date = re.compile(r'"PubDate\\":\\"(.*?)\\"', re.S)
        url = 'http://wenshu.court.gov.cn/CreateContentJS/CreateContentJS.aspx?DocID='
        item_url = self.re_findall(item_url, html)
        item['item_url'] = url + item_url
        item['judge_doc_name'] = self.re_findall(judge_doc_name, html)
        item['judge_code'] = self.re_findall(judge_code, html)
        item['judge_name'] = self.re_findall(judge_name, html)
        show_data = self.re_findall(show_date, html)
        # item['case_type'] = self.re_findall(case_type, html)
        item['case_type'] = '民事案件'
        item['case_reason'] = self.re_findall(case_reason, html)
        item['judge_object'] = self.re_findall(judge_object, html)
        item['judge_rule'] = self.re_findall(judge_rule, html)
        item['doc_head'] = self.re_findall(doc_head, html)
        item['judge_prosecution'] = ''
        if '机关：' in item['doc_head']:
            item['judge_prosecution'] = self.re_findall(judge_prosecution, html)
        if re.findall(doc_truth1, html):
            my_doc_truth2 = re.findall(doc_truth1, html)[0]
            item['doc_truth'] = self.re_findall(doc_truth, html) + my_doc_truth2
        else:
            item['doc_truth'] = self.re_findall(doc_truth, html)
        item['doc_reason'] = self.re_findall(doc_reason, html)
        item['doc_rusult'] = self.re_findall(doc_rusult, html)
        item['doc_bottom'] = self.re_findall(doc_bottom, html)
        item['judge_flg'] = item['case_type'][:-2] + item['judge_process'][:2]
        item['doc_content'] = response.text
        if show_data:
            item['show_date'] = time.strftime("%Y-%m-%d", time.localtime(eval(show_data) / 1000))
        else:
            item['show_date'] = self.re_findall(Pub_date, html)
        if '判决书' in item['judge_doc_name']:
            item['doc_type'] = '判决书'
        elif '裁定书' in item['judge_doc_name']:
            item['doc_type'] = '裁定书'
        elif '调解书' in item['judge_doc_name']:
            item['doc_type'] = '调解书'
        elif '决定书' in item['judge_doc_name']:
            item['doc_type'] = '决定书'
        elif '通知书' in item['judge_doc_name']:
            item['doc_type'] = '通知书'
        else:
            item['doc_type'] = '令'
        # 下载功能暂不启用
        # court_html = re.compile(r'\\"Html\\":\\"(.*?)\\"')
        # read_count = self.re_findall(lookcount, html)
        # court_title = item['judge_doc_name']
        # court_date = item['show_date']
        # court_content = self.re_findall(court_html, html)
        # download_list = [
        #     court_title, court_date, read_count, court_content
        # ]
        # download(download_list, item_url)
        # item['download_url'] = 'judge/%s/%s' % (item_url, download_list[0] + '.doc')
        # print(item['item_url'])
        yield item

    @staticmethod
    def re_findall(pattern, html):
        if re.findall(pattern, html):
            content = re.findall(pattern, html)[0]
            return content
        return ''

    @staticmethod
    def trim_blank(param):
        return re.sub('\s', '', param)

