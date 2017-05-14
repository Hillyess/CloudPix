# -*- coding: utf-8 -*-
import scrapy
import json
import re
import urllib
import os
import HTMLParser
from scrapy.crawler import CrawlerProcess
from CloudPix.items import CloudpixItem
from scrapy.http import Request
from lxml import etree
from scrapy import cmdline
from scrapy import selector


class ArtistSpider(scrapy.Spider):
    name = "Top_New"
    start_urls = [
        "https://www.artstation.com/projects.json?medium=digital2d&page=1&sorting=trending",
        "https://www.artstation.com/projects.json?medium=digital2d&page=2&sorting=trending",
        "https://www.artstation.com/projects.json?medium=digital2d&page=3&sorting=trending"
    ]

    def parse(self, response):  # parse the url to get the json contains artwork list
        jdata = json.loads(response.body)
        total_count = jdata['total_count']
        jdata = jdata['data']

        for permalink in jdata:
            author = permalink['user']['full_name']
            # if permalink['permalink'] not in exisited_link:
            yield scrapy.Request(permalink['permalink'],  meta={'author': author}, callback=self.parse_artwork)

    def parse_artwork(self, response):  # download artwork from pages
        author = response.meta['author']
        htmdata = response.body
        htmdata = str.replace(htmdata, r'\"', '')
        pattern = re.compile(r'image_url:.*width')
        image_url = re.search(pattern, htmdata)
        if image_url:
            mlink = image_url.group(0)
            mlink = mlink[10:-7]
        pattern = re.compile(r'<title>.*?</title>')
        description = re.search(pattern, htmdata).group(0)
        description = str.replace(description, '<title>ArtStation - ', '').replace('</title>', '').replace(',', '-') \
            .replace('?', '')
        html_parser = HTMLParser.HTMLParser()
        description_utf8 = html_parser.unescape(description)
        description_utf8 = replaceillegalfn(description_utf8, ' ')
        item = CloudpixItem()

        pattern = re.compile(r'.*?\.jpg')
        mlink = re.search(pattern, mlink).group(0)
        item['artwork_imgurl'] = mlink  # 提取图片链接
        item['artist'] = author
        item['artwork_description'] = description_utf8
        yield item


def replaceillegalfn(fnstr, alt):  # UTF-8 replace illegal filename
    invalid_characaters = '\\/:*?"<>|'
    for c in invalid_characaters:
        fnstr = fnstr.replace(c, '')
    return fnstr
