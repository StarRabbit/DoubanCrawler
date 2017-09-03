# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DoubanMovieProfileItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    movie_title = scrapy.Field()
    intro = scrapy.Field()
    credit = scrapy.Field()
    judge_crowd = scrapy.Field()
    year = scrapy.Field()
    img_src = scrapy.Field()
    status = scrapy.Field()

class DoubanMovieCommentItem(scrapy.Item):
    author = scrapy.Field()
    comment_text = scrapy.Field()
    credit = scrapy.Field()
    ups = scrapy.Field()
    time = scrapy.Field()
    movie_index = scrapy.Field()

