# -*- coding: utf-8 -*-
import scrapy
import requests

class ZolspiderSpider(scrapy.Spider):
    name = 'Zolspider'
    allowed_domains = ['zol.com.cn']
    start_urls = ['http://detail.zol.com.cn/cell_phone_index/subcate57_list_1.html']
    part_url='http://detail.zol.com.cn'
    def parse(self, response):

        pplist=response.xpath(".//div[@class='brand-list']/a/@href").extract()
        for ppl in pplist:
            ppl=ZolspiderSpider.part_url+ppl
            yield scrapy.Request(
                ppl,
                callback=self.parse_phone_list,
                meta={"item":ppl}
            )

    def parse_phone_list(self,response):
        phone_list_url=response.meta["item"]
        print(phone_list_url)
        for list in phone_list_url:
            item={}
            phone_li_list=response.xpath(".//ul[@id='J_PicMode']/li[starts-with(@data-follow-id,'p')]")
            for phone_li in phone_li_list:
                item["phone_name"]=phone_li.xpath("./h3/a/text()").extract_first()
                item["phone_url"]=phone_li.xpath("./a/@href").extract_first()
                print (item)