# -*- coding: utf-8 -*-
import scrapy
from copy import deepcopy
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
                meta={"item":deepcopy(item)}
                )


    def parse_phone_list(self,response):
        item=deepcopy(response.meta["item"])

        phone_li_list=response.xpath(".//ul[@id='J_PicMode']/li[starts-with(@data-follow-id,'p')]")
        for phone_li in phone_li_list:
            item["phone_name"]=phone_li.xpath("./h3/a/text()").extract_first()
            item["phone_url"]=ZolspiderSpider.part_url+"/"+str((int((phone_li.xpath("./a/@href").extract_first()[17:24])[0:4])+1))+"/"+phone_li.xpath("./a/@href").extract_first()[17:24]+"/param.shtml"
            yield scrapy.Request(
                item["phone_url"],
                callback=self.parse_phone_content,
                meta={"item":deepcopy(item)}
                )
            next_page=phone_li.xpath(".//div[@class='pagebar']/a[@class='next']/@href")
						if next_page is not None:
							 yield scrapy.Request(
                item["next_page"],
                callback=self.parse_phone_list,
                meta={"item":deepcopy(item)}
                )
    def parse_phone_content(self,response):
        item = deepcopy(response.meta["item"])
        if response.xpath(".//div[@class='detailed-parameters']/table[1]/tr[2]/td/span/a/text()").extract_first() is not None:
            if response.xpath(".//div[@class='detailed-parameters']/table[1]/tr[2]/td/span/a/text()").extract_first() =='预约抢购':
                item["Time to market"] = response.xpath(".//div[@class='detailed-parameters']/table[1]/tr[3]/td/span/text()").extract()
            else:
               item["Time to market"]=response.xpath(".//div[@class='detailed-parameters']/table[1]/tr[2]/td/span/a/text()").extract_first()
        else:
           item["Time to market"]=response.xpath(".//div[@class='detailed-parameters']/table[1]/tr[2]/td/span/text()").extract_first()

        yield item

