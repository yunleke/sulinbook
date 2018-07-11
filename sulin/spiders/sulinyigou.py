# -*- coding: utf-8 -*-
import scrapy
from sulin.items import SulinItem
import re
from copy import deepcopy
class SulinyigouSpider(scrapy.Spider):
    name = 'sulinyigou'
    allowed_domains = ['sulin.com']
    start_urls = ['http://snbook.suning.com/web/trd-fl/999999/0.htm']

    def parse(self, response):
        # 获取大分类
        big_sort_list = response.xpath("//div[@class='sider-sort l']//li")
        # 获取小分类
        for li in big_sort_list:
            item = SulinItem()
            item["sm_name"]=li.xpath("./div[@class='three-sort']//a/text()").extract_first()
            item["sm_href"]="http://snbook.suning.com"+li.xpath("./div[@class='three-sort']//a/@href").extract_first()
            #item["sm_href"] =li.xpath("./div[@class='three-sort']//a/@href").extract_first()

            yield scrapy.Request(
                item["sm_href"],
                callback=self.parse_detail,
                meta = {"item":deepcopy(item)},
                dont_filter=True
            )
    def parse_detail(self,response):
        item = response.meta["item"]
        books_li = response.xpath("//div[@class='container']//ul[@class='clearfix']/li")
        for book in books_li:
            item["book_name"] = book.xpath(".//a/text()").extract_first()
            item["book_url"]  = book.xpath(".//a/@href").extract_first()
            yield scrapy.Request(
                item["book_url"],
                callback=self.book_detail,
                meta={"item": deepcopy(item)},
                dont_filter=True
            )
        # 获取当前页码
        sum_page = int(re.findall(r"var pagecount=(.*?);", response.body.decode())[0])
        current_page = int(re.findall(r"var currentPage=(.*?);", response.body.decode())[0])
        if current_page<sum_page:
            item["next_url_start"] = item["sm_href"] + "?pageNumber={}&sort=0".format(current_page+1)
            yield scrapy.Request(
                item["next_url_start"],
                callback = self.parse_detail,
                meta = {"item":item},
                dont_filter = True
            )
    def book_detail(self,response):
        item = response.meta["item"]
        content = response.body.decode()
        #item["book_price"] = response.xpath("//div[@class='ebook-brief']//span[@class='snPrice f18 fl']/em")
        item["book_price"] = re.findall(r"\"bp\":'(.*?)',",content)
        item["book_price"] = item["book_price"][0] if len(item["book_price"]) >0 else None
        yield item
