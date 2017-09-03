# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from .accessory.sql import Sql
from .items import DoubanMovieProfileItem
from scrapy.signals import engine_started,engine_stopped

sql_handler=Sql()
class DoubancrawspiderPipeline(object):
    @classmethod
    def from_crawler(cls,crawler):
        instance = cls()
        global sql_handler
        crawler.signals.connect(sql_handler.db_connect,engine_started)
        crawler.signals.connect(sql_handler.db_teardown,engine_stopped)
        return instance
    def process_item(self, item, spider):
        # print('process_item')
        if isinstance(item, DoubanMovieProfileItem):
            movie_title = item['movie_title']
            year = item['year']
            img_src = item['img_src']
            intro = item['intro']
            credit = item['credit']
            judge_crowd = item['judge_crowd']
            status = item['status']
            sql_handler.insert_into_douban_movies_profile(movie_title,year,img_src,intro,credit,judge_crowd,status)
            print('存储电影信息')
        return item