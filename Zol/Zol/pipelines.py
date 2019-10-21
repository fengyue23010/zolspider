# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json
import pandas as pd
from copy import deepcopy
import csv
class ZolPipeline(object):
    def process_item(self, item, spider):
        # data_csv_ar=[]
        # data_csv_ar.append(deepcopy(item))
        # print(data_csv_ar)
        with open("phone.txt", "a", encoding="utf-8") as f:
            f.write(json.dumps(item, ensure_ascii=False))
            f.write("\n")
        return item
