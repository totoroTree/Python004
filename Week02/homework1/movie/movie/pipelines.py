# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import pymysql
from Week02.homework1.movie.movie import settings


class DbException( Exception ):
    def __init__(self, error_info):
        super().__init__( self, error_info )


'''
Write the crawler results into MySQL database
'''
class MoviePipeline2SQL:
    def __init__(self):
        self.conn = None
        self.cursor = None
        self.items = []

    def db_connection(self):
        # connect the database
        try:
            mysql_conn = pymysql.connect(
                host=settings['MYSQL_HOST'],
                port=settings['MYSQL_PORT'],
                user=settings['MYSQL_USER'],
                passwd=settings['MYSQL_PASSWORD'],
                db=settings['MYSQL_DATABASE'],
                charset=settings['MYSQL_CHARSET']
            )
        except Exception as ex:
            print( ex )
        self.conn = mysql_conn
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        name = item['name']
        category = item['category']
        release_time = item['release_time']
        self.items.append( (name, category, release_time) )
        return item

    def close_spider(self, spider):
        create_table = 'create table if not exists test.movies (name varchar(30), category varchar(30), release_time ' \
                       'varchar(50)) '
        insert_items = 'INSERT INTO movies (name, category, release_time) VALUES (%s, %s, %s)'

        if self.items is not None:
            try:
                # check whether the table exists before inserting anything
                self.cursor.execut( create_table )
                # insert the items into the table
                self.cursor.execut( insert_items, self.items )
                self.conn.commit()
            except Exception as ex:
                raise DbException( 'INSERT failed' )
            # close the db connection
            self.cursor.close()
            self.conn.close()
        else:
            # todo: customize exception
            raise DbException( 'ERROR: MoviePipeline2SQL, no valid movie found' )
