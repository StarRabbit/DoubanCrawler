from bs4 import BeautifulSoup
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider,Rule
from ..items import DoubanMovieProfileItem
# from scrapy.signals import spider_closed,spider_opened
# from scrapy.signalmanager import SignalManager
from pymysql.err import InternalError
from ..accessory.accessories import get_mod_logger



class DoubanCrawSpider(CrawlSpider):
    name = 'doubanspider'
    allowed_domains = ['movie.douban.com']
    download_delay = 0.5
    MAX_PAGE = 168
    base_url = 'https://movie.douban.com/tag/'
    url_pool = []
    logger=get_mod_logger(name)
    for i in range(MAX_PAGE):
        url = base_url+'%E7%A7%91%E5%B9%BB?start={page_index}0&type=T'.format(page_index=2*i)
        url_pool.append(url)

    start_urls = url_pool
    rules = (
        Rule(link_extractor=LinkExtractor(allow='https://movie.douban.com/subject/'),
                  callback='parse_item',follow=False),)
    # 改版一：将sql_handler绑在spider上，这样会有一个问题，当多爬虫运行时数据库链接会冲突
    # @classmethod
    # def from_crawler(cls, crawler, *args, **kwargs):
    #     instance = super().from_crawler(crawler)
    #     database_handler=sql.Sql()
    #     crawler.signals.connect(database_handler.db_connect, signal=spider_opened)
    #     crawler.signals.connect(database_handler.db_teardown,signal=spider_closed)
    #     instance.database_handler = database_handler
    #     instance.signals = crawler.signals
    #     return instance

    def parse_item(self,response):
        self.logger.info('已结完成爬取'+response.url)
        soup = BeautifulSoup(response.text)
        title_node = soup.find('span',{'property':'v:itemreviewed'})
        movie_title = title_node.get_text()
        year = soup.find('span',{'class':'year'}).get_text()[1:5]
        img_src = soup.find('a',{'class':'nbgnbg'}).find('img').get('src')
        intro = soup.find('div',{'id':'info'}).get_text()
        status = ''
        try:
            judge_crowd = soup.find('div',{'class':'rating_self clearfix'}).find('span',{'property':'v:votes'}).get_text()
            credit = soup.find('div', {'class': 'rating_self clearfix'}).find('strong').get_text()
        except:
            judge_crowd = 0
            credit = 0.0
            status = '未上映'
        yield from self.get_item(movie_title,intro,credit,judge_crowd,year,img_src,status)
        # print('parsing item...')

    def get_item(self,movie_title,intro,credit,judge_crowd,year,img_src,status):
        item = DoubanMovieProfileItem()
        item['movie_title']=movie_title
        item['intro']=intro
        item['credit']=credit
        item['judge_crowd']=judge_crowd
        item['year']=year
        item['img_src']=img_src
        item['status']=status
        yield item





