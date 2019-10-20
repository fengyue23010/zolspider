# -*- coding: utf-8 -*-
import scrapy
import requests

class ZolspiderSpider(scrapy.Spider):
    name = 'Zolspider'
    allowed_domains = ['zol.com.cn']
    start_urls = ['http://detail.zol.com.cn/cell_phone_index/subcate57_list_1.html']
    part_url='http://detail.zol.com.cn'
    def parse(self, response):

        pplist=response.xpath(".//div[@class='brand-list']/a")

        for a_list in pplist:
            item = {}
            item["ppname"]=a_list.xpath("./text()").extract_first()
            item["ppurl"]=ZolspiderSpider.part_url+a_list.xpath("./@href").extract_first()
            yield scrapy.Request(
                item["ppurl"],
                callback=self.parse_phone_list,
                meta={"item":item}
                )
            #print(item)

    def parse_phone_list(self,response):
        item=response.meta["item"]
        phone_li_list=response.xpath(".//ul[@id='J_PicMode']/li[starts-with(@data-follow-id,'p')]")
        for phone_li in phone_li_list:
            item["phone_name"]=phone_li.xpath("./h3/a/text()").extract_first()
            item["phone_url"]=ZolspiderSpider.part_url+"/"+str((int((phone_li.xpath("./a/@href").extract_first()[17:24])[0:4])+1))+"/"+phone_li.xpath("./a/@href").extract_first()[17:24]+"/param.shtml"
            yield scrapy.Request(
                item["phone_url"],
                callback=self.parse_phone_content,
                meta={"item": item}
            )
        print(item)
    def parse_phone_content(self,response):
        item=response.meta["item"]
        #print(item)
        # if response.xpath(".//div[@class='detailed-parameters']/table[1]/tr[2]/td/span/text()").extract_first() is not None:
        #     item["shangshishijian"]=response.xpath(".//div[@class='detailed-parameters']/table[1]/tr[2]/td/span/text()").extract_first()
        # else:
        #     item["shangshishijian"]=response.xpath(".//div[@class='detailed-parameters']/table[1]/tr[2]/td/span/a/text()").extract_first()
        #
        # print(item)