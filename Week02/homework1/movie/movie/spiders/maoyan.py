"""
 * Project        Python-Geek-Training
 * (c) copyright  2020
 * Author: Alice Wang

Get the information of top10 movies from Maoyan website
History:
    2020/10/2 initial commit
    2020/10/10 fix issue of hover-tag found nothing
"""

import scrapy
from scrapy import Selector
from movie.items import MovieItem


class MaoyanSpider(scrapy.Spider):
    name = 'maoyan'
    allowed_domains = ['maoyan.com']

    def start_requests(self):
        url = 'https://maoyan.com/films?showType=3'
        # the cookie is read from Firefox explorer
        cookie = 'uuid_n_v=v1; uuid=E8B8B530006811EB8026CDB2BA3E8FD439E453FC2C1D4123A0F9155857AECEC6; ' \
                 'Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1601173617,1601201367,1601207768,1602308468; ' \
                 'mojo-uuid=d6f71e9e9b340709e0abe0b8b5057517; ' \
                 '_lxsdk_cuid=174cd62911662-01d21c8e39ab768-4c3f247a-144000-174cd6291179e; ' \
                 '_lxsdk=E8B8B530006811EB8026CDB2BA3E8FD439E453FC2C1D4123A0F9155857AECEC6; ' \
                 '__mta=250920249.1601173623167.1601208349439.1602308476579.11; ' \
                 '_csrf=3c0198e9cb7b8acf4b41b7463d84c18ab4888a39cff725de3d2dfe15e1409477; ' \
                 'Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1602308468; _lxsdk_s=17511070d75-e2d-fa8-4f3%7C%7C2 '
        yield scrapy.Request(url=url, cookies=cookie, callback=self.parse)


    def parse(self, response):
        # print(response.text)
        counter = 0
        # read the movies' information from HTTP response field 'movie-hover-info'
        candidates = Selector(response=response).xpath('//div[@class="movie-hover-info"]')
        while counter <= 10:
            c_item = candidates[counter]
            item = MovieItem()
            item['name'] = c_item.xpath('./div[1]/span/text()').extract()[0].strip()
            item['category'] = (c_item.xpath('./div[2]/text()').extract()[1]).strip()
            item['release_time'] = (c_item.xpath('./div[4]/text()').extract()[1]).strip()
            # print('-------------------------------------------------------')
            # print(item['name'])
            # print(item['category'])
            # print(item['release_time'])
            counter += 1
            yield item