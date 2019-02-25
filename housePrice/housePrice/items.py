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

class CdfgjItem(scrapy.Item):
    # 楼盘名称
    name = scrapy.Field()

    # 小区地址
    address = scrapy.Field()
    # 面积
    floor_area = scrapy.Field()

    # house type户型
    house_type = scrapy.Field()

    # height高度
    height = scrapy.Field()

    # year_built 建筑年份
    year_built = scrapy.Field()
            
    # 楼盘名称
    name = scrapy.Field()

    # 更新单位，更新时间
    house_update_time = scrapy.Field()
    house_from = scrapy.Field()

    # h_price 单价
    house_h_price = scrapy.Field()

    # total_price 总价格
    house_total_price = scrapy.Field()

    # 房屋信息是否已经进过核验
    house_trust = scrapy.Field()

    # 房屋是否可以售卖
    house_canSale_status = scrapy.Field()

    # 房屋是否有抵押
    house_mortgage_status = scrapy.Field()
    # 房屋核验id
    house_id = scrapy.Field()