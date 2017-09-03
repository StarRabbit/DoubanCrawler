from pymysql import connect
from .. import settings


class Sql():

    def insert_into_douban_movies_profile(self,movie_title,year,img_src,intro,credit,judge_crowd,status):
        sql = 'INSERT INTO douban_movie_profile(movie_title,year,img_src,intro,credit,judge_crowd,status)' \
              'VALUES(%s,%s,%s,%s,%s,%s,%s);'
        value = (movie_title,year,img_src,intro,credit,judge_crowd,status)
        self.cursor.execute(sql,value)
        self.db_connect.commit()

    def db_connect(self):
        # print('db_started')
        self.db_connect = connect(host=settings.MYSQL_HOSTS, port=settings.MYSQL_PORT, user=settings.MYSQL_USER,
                             password=settings.MYSQL_PASSWORD, db=settings.MYSQL_DB, charset='utf8')
        self.cursor = self.db_connect.cursor()

    def db_teardown(self):
        # print('db_teardown')
        self.db_connect.commit()
        self.db_connect.close()








