# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pandas as pd
import csv


class MoviePipeline:
    def __init__(self):
        self.items = []

    def close_spider(self, spider):
        if self.items is not None:
            data = pd.DataFrame(self.items)
            data.to_csv('movies.csv', encoding='utf-8', header=['name', 'category', 'release_time'])
        else:
            print('ERROR: MoviePipeline, no valid movie found')

    def process_item(self, item, spider):
        name = item['name']
        category = item['category']
        release_time = item['release_time']
        self.items.append({'name': name, 'category': category, 'release_time': release_time})
        return item

# Method 2: to write CSV file
# class MoviePipeline2:
    # def __init__(self):
    #     columns = ['name', 'category', 'release_time']
    #     file_name = 'movies.csv'
    #     self.file = open(file_name, 'a+', newline='', encoding='utf-8')
    #     self.writer = csv.writer(self.file)
    #
    # def close_spider(self, spider):
    #     self.file.close()
    #
    # def process_item(self, item, spider):
    #     name = item['name']
    #     category = item['category']
    #     release_time = item['release_time']
    #
    #     print(item['name'])
    #     print(item['category'])
    #     print(item['release_time'])
    #
    #     self.writer.writerow([name, category, release_time])
    #     return item
