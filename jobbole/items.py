# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose
from jobbole.utils.basic import get_num, date_convert, strdate_convert
import re


def get_nums(value):
    match_re = re.match(".*?(\d+).*", value)
    if match_re:
        nums = int(match_re.group(1))
    else:
        nums = 0
    return nums


class JobboleItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class JobboleArticleItemLoader(ItemLoader):
    default_output_processor = TakeFirst()


class JobbolePythonArticleItem(scrapy.Item):
    title = scrapy.Field(
        input_processor=MapCompose(get_num)
    )  # 文章标题
    publish_time = scrapy.Field(
        input_processor=MapCompose(strdate_convert)
    )  # 文章发布时间
    url = scrapy.Field()  # 文章URL
    praise_num = scrapy.Field(
        input_processor=MapCompose(get_num)
    )  # 文章点赞数
    # fav_num = scrapy.Field(
    #     input_processor=MapCompose(get_num)
    # )  # 文章收藏数
    # comment_num = scrapy.Field(
    #     input_processor=MapCompose(get_num)
    # )  # 文章评论数
