# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WenshuSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    item_url = scrapy.Field()
    # download_url = scrapy.Field()
    judge_flg = scrapy.Field()
    judge_doc_name = scrapy.Field()
    judge_code = scrapy.Field()
    judge_reason = scrapy.Field()
    judge_name = scrapy.Field()
    judge_id = scrapy.Field()
    case_type = scrapy.Field()
    case_reason = scrapy.Field()
    judge_process = scrapy.Field()
    judge_date = scrapy.Field()
    judge_prosecution = scrapy.Field()
    judge_object = scrapy.Field()
    judge_rule = scrapy.Field()
    show_date = scrapy.Field()
    doc_content = scrapy.Field()
    doc_head = scrapy.Field()
    doc_truth = scrapy.Field()
    doc_reason = scrapy.Field()
    doc_rusult = scrapy.Field()
    doc_bottom = scrapy.Field()
    doc_type = scrapy.Field()
    isdel = scrapy.Field()
    create_id = scrapy.Field()
    intime = scrapy.Field()
    update_id = scrapy.Field()
    update_time = scrapy.Field()