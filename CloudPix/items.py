# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Join


class CloudpixItemLoader(ItemLoader):
    default_input_processor = MapCompose(str.strip)
    default_output_processor = TakeFirst()
    utc_timestamp_in = TakeFirst()
    name_out = Join()


class CloudpixItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    artist = scrapy.Field()
    view_count = scrapy.Field()
    follower_count = scrapy.Field()
    artwork_count = scrapy.Field()
    artworkurl_list = scrapy.Field()
    artwork_img = scrapy.Field()
    artwork_imgurl = scrapy.Field()
    image_paths = scrapy.Field()
    artwork_description = scrapy.Field()
    pass
