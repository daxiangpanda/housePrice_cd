# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LianjiaItem(scrapy.Item):

    name=scrapy.Field()#楼盘名称

    price=scrapy.Field()#楼盘均价

    district=scrapy.Field()#楼盘所在地区

    landmark=scrapy.Field()#楼盘附近地标

    address=scrapy.Field()#楼盘地址

    floorArea=scrapy.Field()#楼盘建面
