# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SulinItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    book_name = scrapy.Field()
    book_url = scrapy.Field()
    sm_name = scrapy.Field()
    sm_href= scrapy.Field()
    book_price = scrapy.Field()
    book_next_url = scrapy.Field()
    #sum_page = scrapy.Field()
    #current_page = scrapy.Field()
    next_url_start = scrapy.Field()
