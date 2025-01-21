# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class LianjiaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 坐标
    location = scrapy.Field()
    # 小区名字
    name = scrapy.Field()
    # 所属区
    county = scrapy.Field()
    # 价格
    price = scrapy.Field()
    # 交房时间
    delivery_time = scrapy.Field()
    # 开发商
    developer = scrapy.Field()
    # 建筑年代
    building_age = scrapy.Field()